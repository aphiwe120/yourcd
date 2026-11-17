# RLR — Medical Coding Assistant

RLR turns a doctor's plain-language note into the **top 3 South African ICD-10 codes**, each with a one-line reason. Every code is checked against the official **SA ICD-10 Master Industry Table (MIT)**, so it can't suggest a code that doesn't exist. The doctor confirms the right one with one tap.

## Why it matters

Wrong or vague ICD-10 codes get claims rejected or paid from the wrong benefit, and that costs wards money and clinicians time. RLR makes the right code the easiest one to pick.

## How it works

1. The doctor types a note, for example *"type 2 diabetes, poor control, early kidney damage"*.
2. RLR searches the MIT (41,008 codes) and ranks the best matches.
3. It shows three cards, each with the code, the official MIT description, a one-line reason, and a PMB chip when the code is on the CMS Prescribed Minimum Benefits list.
4. The doctor taps **Confirm**, and the choice is saved to their history.

Example: the note above returns **E11.2** (type 2 diabetes with kidney complications) first.

## Stack

- **Front end:** a Node / Next.js page with the mint neumorphic design and healthcare colours
- **Backend:** Python and FastAPI, with the MIT stored in SQLite
- **Data:** the [SA ICD-10 MIT 2021](https://www.health.gov.za/wp-content/uploads/2021/04/ICD-10_MIT_2021_Excel_16-March_2021.xlsx) and the [CMS 2026 PMB coded list](https://www.medicalschemes.co.za/download/2028/icd10-codings/24945/2026-pmb-icd-10-coded-list-distribution.xlsx)
- **AI (optional):** setting `OPENAI_API_KEY` lets a model choose among MIT candidates. Without it, the app runs in MIT search mode. Either way, it can never invent a code.

## Run it locally

```bash
pip install -r requirements.txt
python3 scripts/ingest.py      # builds data/mit.sqlite from the two spreadsheets
npm install
npm run demo                   # app on http://localhost:4317, API on http://localhost:8741/docs
```

Run the tests with `python3 -m pytest -q`.

## API

`POST /api/suggest` with a note returns exactly three MIT-valid codes, each with a description, a reason and a PMB flag. The full schema is at `/docs` while the server is running.

## Scope

This is a hackathon demo. It has no logins and doesn't submit claims, and confirmations are stored locally.

## Team CodePilots

- Mosa Mofokeng
- Aphiwe Mntambo
- George Motlhanke
- Livhuwani Madavha
