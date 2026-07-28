<div align="center">
  <img src="https://img.shields.io/badge/Status-Active-success.svg" alt="Status">
  <img src="https://img.shields.io/badge/License-MIT-blue.svg" alt="License">
  <img src="https://img.shields.io/badge/Python-3.12-blue.svg" alt="Python">
  <img src="https://img.shields.io/badge/React-18-blue.svg" alt="React">
  
  <h1>🚀 CV Tailor (Resume.OS)</h1>
  <p>An autonomous, multi-agent AI system that mathematically engineers your resume to bypass ATS algorithms and secure interviews.</p>
</div>

---

## ⚡ What is CV Tailor?

CV Tailor is a full-stack, AI-powered application that leverages **LangGraph**, **FastAPI**, and **React** to completely automate the resume tailoring process. 

Instead of a basic "wrapper" around ChatGPT, CV Tailor operates as a **Multi-Agent Orchestration Pipeline**. It spins up specialized AI agents (Strategist, Writer, Auditor, ATS Evaluator, and Planner) that iteratively debate, fact-check, and rewrite your resume until it achieves a maximum ATS match score against your target Job Description.

## 🏗️ Architecture & Tech Stack

**Frontend (The "Terminal" Workspace)**
*   **Framework:** React (Vite)
*   **Styling:** Tailwind CSS (Custom Dark Mode "Hacker" aesthetic)
*   **Icons:** Lucide React
*   **Real-time Streaming:** Server-Sent Events (SSE) via custom `useLogStream` hook

**Backend (The AI Engine)**
*   **Framework:** FastAPI (Python)
*   **Database:** PostgreSQL (with SQLAlchemy ORM & Alembic)
*   **Auth:** JWT (JSON Web Tokens) with `passlib` & `bcrypt`
*   **AI Orchestration:** LangGraph, LangChain, OpenAI
*   **Cloud Storage:** Supabase (for storing original & tailored PDFs)
*   **PDF Processing:** PyMuPDF, PDFKit / WeasyPrint

---

## 🧠 The Multi-Agent Pipeline (LangGraph)

When a user initializes the engine, the backend spins up a stateful graph of specialized agents:

```mermaid
graph TD
    Start[User Uploads CV & JD] --> Strategist
    Strategist[🎯 Strategist Agent<br/>Generates Tailoring Plan] --> Writer
    Writer[✍️ Writer Agent<br/>Drafts New Resume] --> Auditor
    Auditor[🛡️ Auditor Agent<br/>Fact-checks Draft] --> ATSEval
    ATSEval[🤖 ATS Evaluator Agent<br/>Scores Draft] --> Planner
    Planner[🗺️ Revision Planner Agent<br/>Decides Next Steps]
    Planner -- Needs Revision --> Writer
    Planner -- Approved --> Finalize[Compile Final PDF]
```

1.  🎯 **The Strategist:** Analyzes the gap between the base resume and the JD. Formulates a 3-point action plan.
2.  ✍️ **The Writer:** Rewrites the resume JSON according to the strategy, optimizing action verbs and keywords.
3.  🛡️ **The Auditor (Fact-Checker):** Strictly compares the new draft against the original resume. If the writer hallucinated or fabricated any skills, the Auditor flags it and forces a rewrite.
4.  🤖 **The ATS Evaluator:** Simulates an enterprise Applicant Tracking System. Scores the draft out of 100%.
5.  🗺️ **The Revision Planner:** Analyzes the ATS score and Auditor feedback. If the score is low or facts were hallucinated, it plans the next loop. Otherwise, it approves the final draft.

---

## 🗄️ Database Design (PostgreSQL)

The system uses a highly relational structure to maintain a full history of user tailorings.

```mermaid
erDiagram
    users ||--o{ resumes : "has"
    users ||--o{ jd : "has"
    users ||--o{ tailored_resume : "has"
    resumes ||--o{ tailored_resume : "source for"
    jd ||--o{ tailored_resume : "target for"

    users {
        int4 id PK
        varchar full_name
        varchar email
        varchar hashed_password
        timestamptz created_at
    }
    resumes {
        int4 id PK
        int4 user_id FK
        varchar original_file_name
        varchar file_path
        json parsed_json
        timestamptz created_at
    }
    jd {
        int4 id PK
        int4 user_id FK
        varchar title
        varchar company
        text raw_text
        json parsed_json
        timestamptz created_at
    }
    tailored_resume {
        int4 id PK
        int4 user_id FK
        int4 original_resume_id FK
        int4 original_jd_id FK
        jsonb tailored_json
        varchar pdf_url
        int4 ats_score
        timestamp created_at
    }
```

*(Note: You can also replace this diagram with your local image screenshot by inserting `![DB Schema](./path-to-your-image.png)`)*

### `users`
*   `id` (PK), `email`, `hashed_password`, `full_name`, `created_at`

### `resumes` (Base Resumes)
*   `id` (PK), `user_id` (FK), `original_file_name`, `file_path` (Supabase URL), `parsed_json`, `created_at`

### `jd` (Job Descriptions)
*   `id` (PK), `user_id` (FK), `title`, `company`, `raw_text`, `parsed_json`, `created_at`

### `tailored_resume` (The Final Outputs)
*   `id` (PK), `user_id` (FK), `original_resume_id` (FK), `original_jd_id` (FK), `tailored_json`, `pdf_url` (Supabase URL), `ats_score`, `created_at`

---

## 🛠️ Step-by-Step Execution Procedure

```mermaid
sequenceDiagram
    participant U as User
    participant F as Frontend (React)
    participant B as Backend (FastAPI)
    participant L as LLM / Agents
    participant S as Supabase Storage
    participant DB as PostgreSQL DB

    U->>F: Upload Resume PDF & Paste JD
    F->>B: POST /upload (Resume)
    B->>S: Upload Original PDF
    B->>DB: Save Resume Record
    B-->>F: return resume_id
    
    F->>B: POST /upload-text (JD)
    B->>DB: Save JD Record
    B-->>F: return jd_id
    
    F->>B: Connect to /run (SSE)
    loop LangGraph Pipeline
        B->>L: Execute Agent Nodes (Strategist, Writer, etc.)
        L-->>B: State Updates
        B-->>F: Stream live logs & UI summaries
    end
    
    B->>S: Upload Tailored PDF
    B->>DB: Save Tailored_Resume Record
    B-->>F: Return Final Download URL
    F-->>U: Show Results Screen
```

1.  **Auth:** User registers/logs in and receives a JWT token.
2.  **Ingestion:** User uploads a PDF resume and pastes JD text.
3.  **Parsing:** Backend uses `PyMuPDF` and LLMs to convert raw text into strict JSON schemas. Original PDF is uploaded to Supabase.
4.  **Orchestration:** Frontend transitions to the "Workspace" and opens an SSE connection to `/api/tailor/run`.
5.  **Streaming:** LangGraph executes. The backend streams live terminal logs and `ui_summary` JSON blocks to the frontend, rendering a beautiful live dashboard.
6.  **Compilation:** Upon completion, the backend compiles the final JSON into a styled PDF, uploads it to Supabase, and saves the `Tailored_Resume` record.
7.  **Delivery:** The frontend receives the final Supabase `download_url` and transitions to the Results screen.

---

## 🔐 Environment Variables (`.env` Template)

Create a `.env` file in the `/backend` directory:

```env
# API Config
PROJECT_NAME="cv_tailor"
API_V1_STR="/api"

# Security
SECRET_KEY="your_super_secret_jwt_key_here"
ACCESS_TOKEN_EXPIRE_MINUTES=11520

# Database
DB_URL="postgresql://user:password@localhost:5432/cv_tailor"

# AI / LLM
API_KEY_LLM="sk-your-openai-or-anthropic-key-here"

# Supabase Storage
SUPABASE_URL="https://your-project.supabase.co"
SUPABASE_PUBLISHABLE_KEY="your_publishable_key"
SUPABASE_SECRET_KEY="your_secret_key"
SUPABASE_JWKS_URL="https://your-project.supabase.co/auth/v1/.well-known/jwks.json"
```

---

## 🔮 Future Works & Roadmap

To scale CV Tailor into a massive production system, the following architectural upgrades are planned:

*   🚀 **Redis Caching Layer:** Implement Redis to cache LLM responses and parsed JD/Resume schemas. This will drastically reduce API costs and latency for repeated job applications.
*   ⚡ **Celery Task Queues:** Move the heavy LangGraph execution into background Celery workers (with RabbitMQ/Redis brokers) to prevent HTTP timeouts and allow infinite horizontal scaling.
*   🧠 **Vector DB Integration (RAG):** Store users' past experiences in Pinecone/Weaviate to allow agents to pull in forgotten achievements dynamically based on the JD.
*   🎨 **Dynamic UI Themes:** Make the terminal look even *crazier* with selectable hacker themes (Matrix Green, Cyberpunk Neon, Synthwave).
*   📊 **Analytics Dashboard:** Build a user dashboard tracking application success rates, average ATS scores, and most frequently matched keywords.
