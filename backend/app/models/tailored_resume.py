from sqlalchemy import null
from sqlalchemy import Column, Integer, String, DateTime, ForeignKey
from sqlalchemy.dialects.postgresql import JSONB
from sqlalchemy.orm import relationship
from datetime import datetime
from app.core.database import Base

class TailoredResume(Base):
    __tablename__ = "tailored_resume"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    original_resume_id = Column(Integer, ForeignKey("resumes.id"), nullable=False)
    original_jd_id = Column(Integer, ForeignKey("jd.id"), nullable=False)

    tailored_json = Column(JSONB, nullable=False)

    pdf_url = Column(String, nullable=True)
    ats_score = Column(Integer, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)

    user = relationship("User", back_populates="tailored_resumes")
    original_resume = relationship("Resume", back_populates="tailored_resumes")
    job_description = relationship("JobDescription")

