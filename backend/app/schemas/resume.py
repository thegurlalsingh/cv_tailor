# We need Pydantic schemas to validate data going in and out of our API (separate from our database models).

from pydantic import BaseModel
from datetime import datetime
from typing import Optional, Dict, Any

# This is what we return to the user
class resume_respone(BaseModel):
    id: int
    user_id: int
    original_file_name: str
    file_path: str
    created_at: datetime

    class config:
        from_attributes = True

# This is the structured data we will extract from the PDF
class parsed_resume_data(BaseModel):
    raw_text: str
    skills: list[str] = []
    experience: list[Dict[str, Any]] = []