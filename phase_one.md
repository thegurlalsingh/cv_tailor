# CVTailor AI - Phase 1: Backend Foundation (Free-Tier First)

Welcome to **Phase 1** of CVTailor AI.  
This phase builds a **production-style backend foundation** for authentication, document ingestion, secure storage, and async processing — while staying **cost-conscious for personal use**.

---

## 🎯 Phase 1 Objectives

- **Authentication:** Secure API access with JWT-based sessions.
- **Document Intake:** Upload resumes (PDF/DOCX) and Job Descriptions (JD file/text).
- **Storage:** S3-compatible object storage for uploaded documents.
- **Asynchronous Processing:** Celery + Redis for background parsing (fast API responses).
- **Database Schema:** PostgreSQL models for users, uploaded files, and parsed text outputs.

---

## 🏗 Architecture & Stack

- **Framework:** FastAPI (Python)
- **Database:** PostgreSQL + SQLAlchemy
- **Queue/Broker:** Celery + Redis
- **Storage:** S3-compatible object storage
- **Authentication:** JWT

### Free-tier-friendly provider options

- **Backend hosting:** Render (free web service + free worker)
- **Postgres:** Neon / Supabase free tier
- **Redis:** Upstash free tier
- **S3-compatible storage:** Cloudflare R2 (or MinIO for local dev)

> You can swap providers later without changing core architecture.

---

## 📂 Directory Structure (Phase 1 Scope)

```text
backend/
├── app/
│   ├── api/v1/endpoints/      # API routes
│   │   ├── auth.py            # /auth/register, /auth/login
│   │   ├── resumes.py         # /resumes/upload
│   │   └── jobs.py            # /jobs/upload, /jobs/text
│   ├── core/                  # config, db, security, logging
│   ├── models/                # SQLAlchemy models
│   │   ├── user.py
│   │   ├── resume.py
│   │   └── job_description.py
│   ├── schemas/               # Pydantic request/response schemas
│   │   ├── auth.py
│   │   ├── resume.py
│   │   └── job.py
│   ├── services/              # business logic
│   │   ├── auth/              # hashing, jwt token logic
│   │   ├── parsing/           # pdf/docx text extraction
│   │   └── storage/           # s3-compatible upload/download
│   └── workers/               # celery app + tasks
│       ├── celery_app.py
│       └── tasks/
│           └── parse_documents.py
├── migrations/                # alembic migrations
├── requirements/              # dependency files
├── .env.example
├── Dockerfile
└── docker-compose.yml
```

---

## 🚀 Getting Started (Local Development)

## Prerequisites

- Docker + Docker Compose
- Python 3.10+
- (Optional local) PostgreSQL, Redis, MinIO via docker-compose

## Setup

1. **Clone repository**
   ```bash
   git clone <repo-url>
   cd cvtailor-ai/backend
   ```

2. **Create env file**
   ```bash
   cp .env.example .env
   ```

3. **Configure environment variables**
   - DB URL
   - Redis URL
   - JWT secret
   - S3-compatible storage credentials (AWS S3 / R2 / MinIO)

4. **Start local infra**
   ```bash
   docker-compose up -d db redis
   ```
   If using MinIO locally, include it in docker-compose and start it too.

5. **Install dependencies**
   ```bash
   python -m venv venv
   source venv/bin/activate  # Windows: venv\Scripts\activate
   pip install -r requirements/dev.txt
   ```

6. **Run DB migrations**
   ```bash
   alembic upgrade head
   ```

7. **Run API**
   ```bash
   uvicorn app.main:app --reload
   ```

8. **Run worker (new terminal)**
   ```bash
   celery -A app.workers.celery_app worker --loglevel=info
   ```

---

## 📜 API Endpoints in Phase 1

## Authentication
- `POST /auth/register` — Register new user
- `POST /auth/login` — Login and receive JWT

## Document Intake
- `POST /resumes/upload` — Upload resume (PDF/DOCX), returns task ID
- `POST /jobs/upload` — Upload JD file
- `POST /jobs/text` — Submit JD as text
- `GET /health` — API + DB health check

---

## ✅ Definition of Done (Phase 1)

- [ ] User registration + login with JWT works.
- [ ] Authorized users can upload PDF/DOCX resumes.
- [ ] Files are stored in configured S3-compatible bucket.
- [ ] Celery worker parses uploaded files asynchronously.
- [ ] Extracted raw text + metadata saved in PostgreSQL.
- [ ] docker-compose reliably starts required services.

---

## 🔒 Security Baseline (Phase 1)

- JWT auth for protected endpoints
- Password hashing (never store plain text)
- Private object storage buckets
- Signed URLs (if direct file access is needed)
- Sensitive configs via environment variables only

---

## 🗺 Next Steps

- **Phase 2:** JD keyword extraction, gap analysis, ATS scoring
- **Phase 3:** Tailoring engine + resume versioning + PDF/DOCX export
- **Phase 4:** Frontend dashboard and preview/download flows