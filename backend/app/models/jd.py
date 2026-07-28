from sqlalchemy import null
from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, JSON, Text
from sqlalchemy.sql import func
from app.core.database import Base
from sqlalchemy.orm import relationship


class JobDescription(Base):
    __tablename__ = "jd"

    id = Column(Integer, primary_key = True, index = True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    title = Column(String, nullable = True)
    company = Column(String, nullable = True)
    raw_text = Column(Text, nullable = False)   
    parsed_json = Column(JSON, nullable = True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())

    user = relationship("User", back_populates="job_descriptions")