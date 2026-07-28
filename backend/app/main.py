from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.core.config import settings
from app.api.endpoints import resumes_router, jd_router, tailor_router, auth_router

app = FastAPI(title = settings.project_name)
origins = [
    "https://cv-tailor-psi.vercel.app/",
]
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
@app.get("/health")
def health_check():
    return {
        "status": "ok",
        "settings": settings.project_name
    }

app.include_router(resumes_router, prefix = "/api")
app.include_router(jd_router, prefix = "/api")
app.include_router(tailor_router, prefix = "/api")
app.include_router(auth_router, prefix = "/api")


