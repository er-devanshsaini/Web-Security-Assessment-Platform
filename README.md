# AI-Powered Web Security Assessment Platform

This project is a student-friendly security assessment platform built in
incremental phases. It analyzes HTTP security posture, can run authorized Nmap
reconnaissance, scores risk, generates PDF reports, and presents results in a
React dashboard.

## Current Status

Implemented phases:

- Phase 1: FastAPI backend, config, health check, SQLite setup
- Phase 2: website scanning, HTTP analysis, missing header detection
- Phase 3: Nmap integration and open service storage
- Phase 4: OWASP-oriented checks for CSP, HSTS, cookies, authentication
- Phase 5: risk scoring and severity prioritization
- Phase 6: PDF report generation
- Phase 7: React dashboard with charts and report downloads
- Phase 8: local AI-style security assistant explanations

## Folder Structure

```text
security-assessment-platform/
├── backend/
├── frontend/
├── database/
├── reports/
├── docs/
├── tests/
└── docker/
```

## Run The Backend

```bash
cd backend
python -m venv .venv
.venv\Scripts\activate
pip install -r requirements.txt
uvicorn app.main:app --reload
```

Health check:

```bash
curl http://127.0.0.1:8000/api/health
```

Local settings use the `SAP_` prefix, for example `SAP_DATABASE_URL`. The
prefix keeps this app from accidentally reading unrelated system variables such
as `DEBUG`.

## Run The Frontend

```bash
cd frontend
npm install
npm run dev
```

Open:

```text
http://127.0.0.1:5173
```

## How A Scan Works

1. The dashboard sends `POST /api/scans` with a target URL.
2. The backend fetches the website with `httpx`.
3. Security headers, HTTPS behavior, cookies, and authentication hints are checked.
4. Optional Nmap reconnaissance runs against the hostname.
5. Findings are scored and saved in SQLite.
6. A PDF report is generated in `reports/`.
7. The dashboard loads findings, charts, assistant guidance, and report links.

Only scan systems you own or have explicit permission to test.

## Learning Goal

The code is intentionally readable and practical. It is designed to show the
kind of engineering habits expected in Product Security, Cyber Security, and
Security Analyst internship interviews.
