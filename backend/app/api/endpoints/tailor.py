from starlette.responses import StreamingResponse
from starlette.responses import FileResponse
from fastapi import APIRouter, Body, Depends
from app.models.user import User
from app.core.database import get_db
from app.api.deps import current_user
from app.models.tailored_resume import TailoredResume
from sqlalchemy.orm import Session
from app.services.tailoring.graph import app as tailor_graph
from app.services.export.supabase_client import upload_pdf_to_supabase
from app.services.export.pdf_exporter import generate_pdf_from_json
import uuid
import json
import asyncio

router = APIRouter()

@router.post("/run")
async def run_tailoring(
    original_resume_json: dict = Body(..., embed=True),
    job_description_json: dict = Body(..., embed=True),
    resume_id: int = Body(..., embed=True),  # We need these from frontend now
    jd_id: int = Body(..., embed=True),
    current_user: User = Depends(current_user), # Secures the endpoint
    db: Session = Depends(get_db)
):

    initial_state = {
        "original_resume_json": original_resume_json,
        "job_description_json": job_description_json,
        "tailoring_plan": "",
        "current_draft_json": {},
        "auditor_feedback": [],
        "ats_score": 0,
        "loop_count": 0
    }
    

    async def event_generator():
        yield f"data: {json.dumps({'log': 'System: Initialization complete. Waking up agents...'})}\n\n"
        await asyncio.sleep(0.5)
        final_state_data = initial_state.copy()

        async for event in tailor_graph.astream(initial_state):
            for node_name, node_state in event.items():
                summary_key = f"{node_name}_summary"
                ui_summary = node_state.get(summary_key, None)

                if node_name == "strategist":
                    log_message = f"INFO  STRATEGIST: Analysis complete. Plan generated."

                elif node_name == "writer":
                    log_message = f"RUNNING  WRITER: Resume draft updated."

                elif node_name == "auditor":
                    feedback = node_state.get("auditor_feedback", [])
                    if feedback:
                        log_message = f"WARNING  AUDITOR: Hallucination detected — {feedback[0]}"
                    else:
                        log_message = f"INFO  AUDITOR: All facts verified. No hallucinations found."
                
                elif node_name == "ats_evaluator":
                    ats_report = node_state.get("ats_report", {})
                    score = ats_report.get("overall_score", "N/A")
                    log_message = f"SYNC  ATS_EVALUATOR: Score updated → {score}%"
                
                elif node_name == "revision_planner":
                    log_message = f"INFO  REVISION_PLANNER: Next revision strategy prepared."
                else:
                    log_message = f"INFO  [{node_name.upper()}] Task completed."

                chunk = {
                    "node": node_name,
                    "log": log_message,
                    "ui_summary": ui_summary,  # This is what the frontend terminal will display!
                    "state_updates": node_state
                }

                yield f"data: {json.dumps(chunk)}\n\n"

                final_state_data.update(node_state)

        yield f"data: {json.dumps({'log': 'System: Agents finished. Generating PDF...'})}\n\n"

        if final_state_data and "current_draft_json" in final_state_data:
            filename = f"tailored_{uuid.uuid4().hex[:8]}.pdf"
            pdf_path = generate_pdf_from_json(final_state_data["current_draft_json"], filename)

            yield f"data: {json.dumps({'log': 'System: Uploading to cloud storage...'})}\n\n"

            supabase_path = f"{current_user.id}/{filename}"
            public_url = upload_pdf_to_supabase(pdf_path, supabase_path, "tailored_resumes")

            yield f"data: {json.dumps({'log': 'System: Saving results to database...'})}\n\n"

            new_tailored_resume = TailoredResume(
                user_id= current_user.id,
                original_resume_id = resume_id,
                original_jd_id = jd_id,
                tailored_json = final_state_data["current_draft_json"],
                pdf_url = public_url,
                ats_score = final_state_data["ats_score"]
            )

            try:
                db.add(new_tailored_resume)
                db.commit()
                db.refresh(new_tailored_resume)
                print("ID:", new_tailored_resume.id)
                print("USER ID:", new_tailored_resume.user_id)
            
            except Exception as e:
                db.rollback()
                print("DB ERROR:", e)
                raise

            yield f"data: {json.dumps({'log': 'System: PDF Ready!', 'download_url': public_url})}\n\n"

        else:
            yield f"data: {json.dumps({'log': 'System: Error generating final PDF.'})}\n\n"

    return StreamingResponse(event_generator(), media_type = "text/event-stream")
            


            
    # final_state = await tailor_graph.ainvoke(initial_state)
    # final_resume = final_state["current_draft_json"]

    # output_filename = "tailored_resume_output.pdf"
    # pdf_path = generate_pdf_from_json(final_resume, output_filename)

    # return FileResponse(
    #     path = pdf_path,
    #     filename = "Tailored_Resume.pdf",
    #     media_type = "application/pdf"
    # )
