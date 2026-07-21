<div align="center">

# 🔐 Biometric Consent & Policy Enforcement Framework

### Samsung PRISM Research Project

**Week 3 – Backend Foundation & Database Infrastructure**

![Python](https://img.shields.io/badge/Python-3.14-blue?logo=python)
![FastAPI](https://img.shields.io/badge/FastAPI-0.116-green?logo=fastapi)
![SQLAlchemy](https://img.shields.io/badge/SQLAlchemy-2.x-red)
![PostgreSQL](https://img.shields.io/badge/PostgreSQL-17-blue?logo=postgresql)
![Alembic](https://img.shields.io/badge/Alembic-Migrations-orange)
![Status](https://img.shields.io/badge/Status-Week%203%20Complete-success)

</div>

---

# 📖 Overview

This repository contains the **Week 3 implementation** of the **Biometric Consent & Policy Enforcement Framework** developed as part of the **Samsung PRISM Research Program**.

Following the software architecture designed in Week 2, this phase establishes the **backend foundation** required for future implementation of biometric consent lifecycle management, policy evaluation, and secure authorization workflows.

The implementation focuses exclusively on backend infrastructure and intentionally excludes business logic to maintain a layered and scalable architecture.

---

# 🎯 Week 3 Objectives

- Initialize a scalable FastAPI backend project
- Configure PostgreSQL database connectivity
- Design normalized database schema
- Implement SQLAlchemy ORM models
- Develop Pydantic schema layer
- Configure Alembic database migrations
- Establish application configuration management
- Verify backend startup and database connectivity

---

# 🏗️ System Architecture

```
                FastAPI Application
                        │
        ┌───────────────┼───────────────┐
        │               │               │
        ▼               ▼               ▼
 Configuration     SQLAlchemy ORM    Pydantic Schemas
        │               │               │
        └───────────────┼───────────────┘
                        │
                        ▼
                 PostgreSQL Database
                        │
                        ▼
              Alembic Migration Layer
```

---

# 📂 Project Structure

```text
Implementation/
│
├── app/
│   ├── api/
│   ├── core/
│   │   ├── config.py
│   │   └── security.py
│   │
│   ├── database/
│   │   ├── base.py
│   │   └── database.py
│   │
│   ├── models/
│   │   ├── consent.py
│   │   ├── policy.py
│   │   ├── audit_log.py
│   │   ├── enums.py
│   │   └── __init__.py
│   │
│   ├── schemas/
│   │   ├── consent.py
│   │   ├── policy.py
│   │   ├── audit_log.py
│   │   ├── common.py
│   │   ├── enums.py
│   │   └── __init__.py
│   │
│   ├── services/
│   ├── utils/
│   └── main.py
│
├── alembic/
├── requirements.txt
├── .env.example
├── alembic.ini
└── README.md
```

---

# 🛠️ Technology Stack

| Layer | Technology |
|--------|------------|
| Programming Language | Python 3.14 |
| Backend Framework | FastAPI |
| ORM | SQLAlchemy 2.x |
| Database | PostgreSQL |
| Validation | Pydantic v2 |
| Database Migration | Alembic |
| ASGI Server | Uvicorn |

---

# 🗄️ Database Design

The database layer consists of three primary entities:

### Consent

Stores biometric consent metadata, including user information, biometric type, processing purpose, consent status, lifecycle timestamps, and versioning.

### Policy

Represents authorization policies that will be evaluated during future consent verification and authorization workflows.

### Audit Log

Maintains immutable audit records for future authorization decisions and compliance tracking.

---

# ⚙️ Backend Components

## FastAPI Application

- Modular project initialization
- Environment-based configuration
- Structured application startup
- Ready for future API integration

---

## SQLAlchemy ORM

Implemented using SQLAlchemy 2.x Declarative Mapping.

Features include:

- UUID Primary Keys
- Enumerations
- Relationships
- Indexed Columns
- Timezone-aware timestamps

---

## Pydantic Schema Layer

Separate schemas are provided for:

- Create Requests
- Update Requests
- Response Models
- Common API Responses

This separation ensures strong validation while keeping persistence and API layers independent.

---

## Alembic Migration

Database versioning is managed using Alembic.

Current migration:

```
0001_initial_schema.py
```

Creates:

- consents
- policies
- audit_logs

---

# 🚀 Getting Started

## Create Virtual Environment

```bash
python -m venv venv
```

Activate:

### Windows

```powershell
.\venv\Scripts\Activate.ps1
```

### Linux/macOS

```bash
source venv/bin/activate
```

Install dependencies:

```bash
pip install -r requirements.txt
```

---

# 🔧 Environment Configuration

Create a local environment file.

```bash
cp .env.example .env
```

Configure:

```env
DATABASE_URL=postgresql://username:password@localhost:5432/biometric_db

SECRET_KEY=your_secret_key

ALGORITHM=HS256

ACCESS_TOKEN_EXPIRE_MINUTES=30
```

---

# 🗃️ Database Migration

Generate migration:

```bash
alembic revision --autogenerate -m "Initial schema"
```

Apply migration:

```bash
alembic upgrade head
```

---

# ▶️ Running the Application

```bash
python -m uvicorn app.main:app --reload
```

Application URL

```
http://127.0.0.1:8000
```

Swagger UI

```
http://127.0.0.1:8000/docs
```

---

# ✅ Week 3 Deliverables

- ✔ FastAPI backend initialization
- ✔ PostgreSQL integration
- ✔ SQLAlchemy ORM models
- ✔ Pydantic validation layer
- ✔ Alembic configuration
- ✔ Initial database migration
- ✔ Environment configuration
- ✔ Backend startup verification

---

# 🚧 Future Scope

The following components are intentionally excluded from Week 3 and will be implemented in subsequent phases:

- Biometric Consent Manager
- Policy Decision Engine
- Access Enforcement Module
- JWT Authentication
- REST API Endpoints
- Authorization Workflow
- Audit Event Publishing

---

<div align="center">

### Samsung PRISM Research Project

**Week 3 Milestone Completed Successfully** 🚀

</div>
