from fastapi import APIRouter
from endpoints import resumes, jd, tailor, auth


api_router = APIRouter()
api_router.include_router(resumes.router, prefix = "/resumes", tags = ["resumes"])
api_router.include_router(jd.router, prefix = "/jd", tags = ["jd"])
api_router.include_router(tailor.router, prefix = "/tailor", tags = ["tailor"])
api_router.include_router(auth.router, prefix = "/auth", tags = ["auth"])


