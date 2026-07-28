from app.services.export.supabase_client import upload_pdf_to_supabase
from langchain_core.utils import uuid
from app.services.parsing import extract_text_from_pdf
from fastapi import APIRouter, Depends, UploadFile, File, HTTPException
from sqlalchemy.orm import Session
from app.core.database import get_db
from app.api.deps import current_user
from app.models.user import User
from app.models.resume import Resume
from app.services.llm import structured_resume_text
import uuid
import json
import os

router = APIRouter()

@router.post("/upload")
async def upload_file(file: UploadFile = File(...), db: Session = Depends(get_db), current_user: User = Depends(current_user)):
    if not file.filename.endswith(('.pdf', '.docx')):
        raise HTTPException(status_code = 400, detail = "Only pdf and docx files are allowed")
    
    file_bytes = await file.read()
    extracted_text = ""
    if file.filename.endswith('.pdf'):
        extracted_text = extract_text_from_pdf(file_bytes)
    
    if not extracted_text:
         raise HTTPException(status_code=400, detail="Could not extract text from file")

    json_resume_data = await structured_resume_text(extracted_text)

    # print("=" * 50)
    # print(extracted_text[:4000])
    # print("=" * 50)


    
    # print("=" * 50)
    # print("PARSED RESUME JSON")
    # print("=" * 50)
    # print(json.dumps(json_resume_data, indent=4))


    


    # Add uploading to supabase after whole debugging will end

    # temp_filename = f"{uuid.uuid4().hex}_{file.filename}"
    # with open(temp_filename, "wb") as f:
    #     f.write(file_bytes)
    
    # try:
    #     supabase_path = f"{current_user.id}/original_{file.filename}"
    #     public_url = upload_pdf_to_supabase(temp_filename, supabase_path, "original_resumes")
    
    # except Exception as e:
    #     if os.path.exists(temp_filename):
    #         os.remove(temp_filename)
    #     raise HTTPException(status_code=500, detail=f"Failed to upload to cloud: {e}")

    # if os.path.exists(temp_filename):
    #     os.remove(temp_filename)

    new_resume = Resume(
        user_id = current_user.id,
        original_file_name = file.filename,
        # file_path = public_url,
        file_path = "",
        parsed_json = json.loads(json_resume_data) if isinstance(json_resume_data, str) else json_resume_data
    ) 
    try:
        db.add(new_resume)
        db.commit()
        db.refresh(new_resume)
        print("ID:", new_resume.id)
        print("User:", new_resume.user_id)

    except Exception as e:
        db.rollback()
        print("DB ERROR:", e)
        raise
        

    return {
        "resume_id": new_resume.id,
        "original_resume_file_url": file.filename,
        "filename": file.filename,
        "content_type": file.content_type,
        "message": "File received successfully. Parsing pending",
        "preview_of_json_output": new_resume.parsed_json
    }