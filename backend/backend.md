# Excel Q&A Backend: GitHub Copilot Implementation Prompts

Architecture: Text-to-SQL / hybrid SQL + vector RAG over ~50,000 Excel rows.
Stack: Pandas + DuckDB, LlamaIndex (NLSQLTableQueryEngine), optional Chroma, cloud LLM (OpenAI / Anthropic / Gemini), FastAPI + vanilla HTML5 front end.

Run the prompts in order and check that each step works before moving on.

---

## Prompt 1: Ingest the Excel file into DuckDB

```
Create a Python module `ingest.py` that loads an Excel file into a local DuckDB database.

Requirements:
- Use pandas (`read_excel`, openpyxl engine) to load the file; path comes from a CLI arg or env var `EXCEL_PATH`.
- Normalise column names to snake_case, strip whitespace, and infer sensible dtypes (dates, numerics).
- Write the DataFrame to a persistent DuckDB file `data.duckdb` as table `records` (replace if exists).
- Expect ~50,000 rows; use DuckDB's direct DataFrame registration for speed, not row-by-row inserts.
- Print row count, column names and dtypes after loading.
- Add a `requirements.txt` with pandas, openpyxl, duckdb.
- Include a small pytest test that ingests a tiny sample DataFrame and asserts the row count matches.
```

---

## Prompt 2: Text-to-SQL query engine with LlamaIndex

```
Create `query_engine.py` that answers natural-language questions over the DuckDB `records` table using LlamaIndex's NLSQLTableQueryEngine.

Requirements:
- Connect to `data.duckdb` via SQLAlchemy (duckdb-engine) and wrap it in LlamaIndex `SQLDatabase`, restricted to the `records` table.
- Configure the LLM from env vars: `LLM_PROVIDER` (openai | anthropic | gemini) and the matching API key. Default to OpenAI.
- Only the schema and a few sample rows should be sent to the LLM; the SQL must run locally on the full table.
- Return both the natural-language answer and the generated SQL (from response metadata) so results can be audited.
- Guardrails: allow only read-only SELECT statements; reject anything with INSERT/UPDATE/DELETE/DROP/ALTER.
- Add a simple CLI loop: `python query_engine.py` prompts for a question, prints the SQL and the answer.
- Add llama-index, llama-index-llms-openai, llama-index-llms-anthropic, llama-index-llms-gemini, sqlalchemy, duckdb-engine to requirements.
- Write tests for counting, filtering and aggregation questions (mock the LLM to return fixed SQL) and for the read-only guard.
```

---

## Prompt 3: Optional vector search for long text columns (hybrid routing)

```
Add optional semantic search for long free-text columns and route questions between SQL and vector search.

Requirements:
- In `vector_index.py`, detect text columns whose average length exceeds a threshold (configurable, default 100 chars), or accept an explicit list via config.
- Embed those columns with the row's primary key as metadata and store them in a persistent Chroma collection (`./chroma_db`). Make it idempotent: skip rebuild if the index matches the current row count.
- In `hybrid_engine.py`, use LlamaIndex `RouterQueryEngine` (or SQLAutoVectorQueryEngine) with two tools:
  - the NLSQLTableQueryEngine from query_engine.py for counts, filters, maths and aggregations
  - a vector query engine for semantic questions ("what do customers complain about...")
- Support combined questions by letting vector results return row IDs that can then be filtered with SQL.
- If no long text columns exist, skip the vector index entirely and fall back to SQL-only.
- Update the CLI to use the hybrid engine and print which route was chosen.
- Add chromadb and llama-index-vector-stores-chroma to requirements; add tests for routing with a mocked LLM.
```

---

## Prompt 4: FastAPI backend serving a vanilla HTML5 front end

```
Wrap the hybrid query engine in a FastAPI backend that serves a vanilla HTML5/CSS/JS front end (no frameworks, no build step).

Backend (`app.py`):
- Create the FastAPI app and initialise the hybrid engine once at startup (lifespan handler), not per request.
- Routes:
  - GET  /                -> serve `static/index.html`
  - GET  /static/*        -> mount `static/` with StaticFiles for CSS/JS
  - POST /api/query       -> body `{ "question": str }`, returns `{ "answer": str, "sql": str | null, "route": "sql" | "vector", "rows": list | null }`
  - GET  /api/schema      -> returns table name, columns and dtypes from DuckDB
  - GET  /api/health      -> `{ "status": "ok", "row_count": int }`
  - POST /api/ingest      -> multipart Excel upload; re-runs ingest.py logic and rebuilds the vector index if needed
- Use Pydantic models for request/response bodies.
- Return clear JSON errors (400 for empty question, 422 for rejected non-SELECT SQL, 500 for LLM failures) without leaking API keys or stack traces.
- Run blocking engine calls in a threadpool (`run_in_threadpool`) so the event loop isn't blocked.
- Enable CORS only for localhost during development.

Front end (`static/index.html`, `static/style.css`, `static/app.js`):
- Semantic HTML5: a header, a form with a textarea and Ask button, and a results section.
- `app.js` uses `fetch` to POST to /api/query, shows a loading state, and disables the button while waiting.
- Render the answer, a collapsible <details> block showing the generated SQL and route, and an HTML <table> for any returned rows.
- On load, call /api/schema and list the available columns so users know what they can ask about.
- Add a file input that uploads a new Excel file to /api/ingest and shows the new row count.
- Escape all rendered text (use textContent, never innerHTML with user/LLM data).
- Keep the CSS simple and responsive.

Also:
- Add fastapi, uvicorn[standard] and python-multipart to requirements.txt.
- Add a README section: `uvicorn app:app --reload`, then open http://localhost:8000.
- Write pytest tests using FastAPI's TestClient for /api/health, /api/query (with the engine mocked) and the error cases.
```
