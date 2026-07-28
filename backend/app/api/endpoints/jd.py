from app.models import user
import json
from fastapi import APIRouter, Depends, Body, HTTPException
from sqlalchemy.orm import Session
from app.core.database import get_db
from app.models.jd import JobDescription
from app.api.deps import current_user
from app.models.user import User
from app.services.llm import structured_jd_text

router = APIRouter()

@router.post("/upload-text")
async def upload_file(raw_text: str = Body(..., media_type="text/plain"), db: Session = Depends(get_db), user: User = Depends(current_user)):
    if not raw_text or len(raw_text) < 50:
        raise HTTPException(status_code = 400, detail = "Please put job description properly or its too short!")

    print(raw_text)

    json_jd = await structured_jd_text(raw_text)

    parsed_dict = json.loads(json_jd) if isinstance(json_jd, str) else json_jd

    # print("=" * 50)
    # print("PARSED JD JSON")
    # print("=" * 50)
    # print(json.dumps(json_jd, indent=4))

    new_jd = JobDescription(
        user_id = user.id,
        raw_text = raw_text,
        title = parsed_dict.get("job_title", "Unknown Title"),
        company = parsed_dict.get("company_name", "Unknown Company"),
        parsed_json = parsed_dict
    )
    try:
        db.add(new_jd)
        db.commit()
        db.refresh(new_jd)

        print("ID:", new_jd.id)
        print("USER ID:", new_jd.user_id)
    
    except Exception as e:
        db.rollback()
        print("DB ERROR:", e)
        raise

    return {
        "jd_id": new_jd.id,
        "message": "Text received successfully. strcuturing pending",
        "preview_of_json_output": new_jd.parsed_json
    }