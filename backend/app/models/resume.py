from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, JSON
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship
from app.core.database import Base

class Resume(Base):
    __tablename__ = "resumes"

    id = Column(Integer, primary_key = True, index = True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable = False)
    original_file_name = Column(String, nullable = False) 
    file_path = Column(String, nullable = False) 
    parsed_json = Column(JSON, nullable = False) 
    created_at = Column(DateTime(timezone = True), server_default = func.now())

    user = relationship("User", back_populates="resumes")
    tailored_resumes = relationship("TailoredResume",back_populates="original_resume")
    
