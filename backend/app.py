"""
FastAPI backend serving the Q&A application.

Provides REST API endpoints and serves static HTML/CSS/JS frontend.
"""

import os
from contextlib import asynccontextmanager
from fastapi import FastAPI, HTTPException, UploadFile, File
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import Optional, List, Dict, Any
from fastapi.concurrency import run_in_threadpool
import duckdb
from ingest import ingest
from hybrid_engine import HybridEngine


# Models
class QueryRequest(BaseModel):
    question: str


class QueryResponse(BaseModel):
    answer: str
    sql: Optional[str] = None
    route: Optional[str] = None
    rows: Optional[List[Dict[str, Any]]] = None


class SchemaResponse(BaseModel):
    table_name: str
    columns: Dict[str, str]


class HealthResponse(BaseModel):
    status: str
    row_count: int


# Global engine
engine = None


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Lifespan context manager for startup/shutdown."""
    global engine
    engine = HybridEngine()
    print("[OK] Query engine initialized")
    yield
    print("[OK] Shutting down")


app = FastAPI(title="Medical Coding Assistant - Backend", lifespan=lifespan)

# CORS for localhost
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost", "http://localhost:*", "http://127.0.0.1:*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/")
async def serve_index():
    """Serve the main HTML page."""
    static_dir = os.path.join(os.path.dirname(__file__), 'static')
    return FileResponse(os.path.join(static_dir, 'index.html'))


@app.get("/static/{path:path}")
async def serve_static(path: str):
    """Serve static assets (CSS, JS)."""
    static_dir = os.path.join(os.path.dirname(__file__), 'static')
    file_path = os.path.join(static_dir, path)
    if not os.path.exists(file_path):
        raise HTTPException(status_code=404, detail="File not found")
    return FileResponse(file_path)


@app.post("/api/query", response_model=QueryResponse)
async def query(request: QueryRequest):
    """Execute a natural language query."""
    global engine
    
    if not request.question.strip():
        raise HTTPException(status_code=400, detail="Question cannot be empty")
    
    try:
        result = await run_in_threadpool(engine.query, request.question)
        
        if 'error' in result:
            raise HTTPException(status_code=422, detail=result['error'])
        
        return result
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Query failed: {str(e)}")


@app.get("/api/schema", response_model=SchemaResponse)
async def schema():
    """Return database schema."""
    try:
        conn = duckdb.connect('data.duckdb')
        schema_info = conn.execute("DESCRIBE records").fetchall()
        columns = {col[0]: col[1] for col in schema_info}
        conn.close()
        
        return SchemaResponse(table_name='records', columns=columns)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Schema retrieval failed: {str(e)}")


@app.get("/api/health", response_model=HealthResponse)
async def health():
    """Health check endpoint."""
    try:
        conn = duckdb.connect('data.duckdb')
        row_count = conn.execute("SELECT COUNT(*) FROM records").fetchone()[0]
        conn.close()
        
        return HealthResponse(status='ok', row_count=row_count)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Health check failed: {str(e)}")


@app.post("/api/ingest")
async def upload_and_ingest(file: UploadFile = File(...)):
    """Upload and ingest a new Excel file."""
    try:
        # Save uploaded file
        upload_dir = '/tmp'
        file_path = os.path.join(upload_dir, file.filename)
        
        contents = await file.read()
        with open(file_path, 'wb') as f:
            f.write(contents)
        
        # Ingest the file
        await run_in_threadpool(ingest, file_path)
        
        # Return new row count
        conn = duckdb.connect('data.duckdb')
        row_count = conn.execute("SELECT COUNT(*) FROM records").fetchone()[0]
        conn.close()
        
        return {'status': 'ok', 'row_count': row_count}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Ingest failed: {str(e)}")


if __name__ == '__main__':
    import uvicorn
    uvicorn.run(app, host='0.0.0.0', port=8000, reload=True)


