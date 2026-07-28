from .resumes import router as resumes_router
from .jd import router as jd_router
from .tailor import router as tailor_router
from .auth import router as auth_router

__all__ = [
    "resumes_router",
    "jd_router",
    "tailor_router",
    "auth_router"
]