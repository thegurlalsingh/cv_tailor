from sqlalchemy import Column, Integer, String, DateTime
from sqlalchemy.sql import func
from app.core.database import Base
from sqlalchemy.orm import relationship

class User(Base):
    __tablename__ = "users"
    
    id = Column(Integer, primary_key = True, index = True)
    full_name = Column(String, nullable=False)
    email = Column(String, unique = True, index = True, nullable = False)
    hashed_password = Column(String, nullable = False) # two users can have same hash value
    created_at = Column(DateTime(timezone = True), server_default = func.now())
    
    resumes = relationship("Resume", back_populates = "user", cascade="all, delete-orphan")
    job_descriptions = relationship("JobDescription", back_populates="user", cascade="all, delete-orphan")
    tailored_resumes = relationship("TailoredResume", back_populates="user", cascade="all, delete-orphan")