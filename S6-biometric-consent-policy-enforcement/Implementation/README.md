# Biometric Consent & Policy Enforcement Framework

## Project Overview

This repository contains the Phase 1 backend skeleton for the Samsung PRISM
research project, **Biometric Consent & Policy Enforcement Framework**.

Phase 1 focuses only on project initialization and backend architecture. Consent
management, policy evaluation, access enforcement, and domain-specific API
endpoints will be implemented in later phases.

## Tech Stack

- Python 3.14
- FastAPI
- PostgreSQL
- SQLAlchemy ORM
- Alembic
- Pydantic
- JWT Authentication
- Uvicorn

## Folder Structure

```text
implementation/
├── app/
│   ├── api/
│   ├── core/
│   │   ├── config.py
│   │   └── security.py
│   ├── database/
│   │   ├── base.py
│   │   └── database.py
│   ├── models/
│   ├── schemas/
│   ├── services/
│   ├── utils/
│   └── main.py
├── alembic/
│   └── versions/
├── alembic.ini
├── requirements.txt
├── .env.example
├── .gitignore
└── README.md
```

## How to Install

Create and activate a virtual environment:

```bash
python -m venv venv
source venv/bin/activate
```

On Windows PowerShell:

```powershell
python -m venv venv
.\venv\Scripts\Activate.ps1
```

Install dependencies:

```bash
pip install -r requirements.txt
```

Create a local environment file:

```bash
cp .env.example .env
```

Update `.env` with your local PostgreSQL database URL and secret values.

## Environment Setup

Copy the example environment file:

```bash
cp .env.example .env
```

On Windows PowerShell:

```powershell
Copy-Item .env.example .env
```

Configure `DATABASE_URL` with your local PostgreSQL connection string.

Configure `SECRET_KEY` with a secure development secret.

Run the application:

```bash
python -m uvicorn app.main:app --reload
```

## How to Run

Start the FastAPI development server:

```bash
python -m uvicorn app.main:app --reload
```

Open the root endpoint:

```text
GET http://127.0.0.1:8000/
```

Expected response:

```json
{
  "project": "Biometric Consent & Policy Enforcement Framework",
  "status": "Running"
}
```

## Alembic

Alembic is configured for future migrations and points to the shared SQLAlchemy
metadata in `app.database.base`. No database tables or domain models are created
in Phase 1.
