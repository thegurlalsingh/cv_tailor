# The state is what our agents will pass back and forth.

import operator
from typing import TypedDict, Annotated, List, Dict

class tailor_state(TypedDict):
    original_resume_json: dict
    job_description_json: dict

    tailoring_plan: List[str] # Updated by strategist agent
    current_draft_json: dict # Updated by writer agent

    auditor_feedback: Annotated[List[str], operator.add]
    ats_score: int # Updated by ATS Evaluator
    ats_report: dict
    revision_plan: Dict
    loop_count: int # Safety mechanism to prevent infinte loops
    strategist_summary: Dict
    writer_summary: Dict
    auditor_summary: Dict
    ats_evaluator_summary: Dict
    revision_planner_summary: Dict