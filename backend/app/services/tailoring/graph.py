# Create the graph that links our agents together

import json
from langgraph.graph import StateGraph, END
from .state import tailor_state
import json
from app.services.llm.provider import llm_for_agent
from app.services.export.pdf_exporter import generate_pdf_from_json

async def strategist_node(state: tailor_state):
    # Compare this Resume to this Job Description and Write a 3-bullet point plan on how to tailor the resume to fit the JD better. Focus on which keywords to add and which experiences to highlight.
    print("Strategist is creating a plan")

    prompt = f"""
You are an expert Resume Tailoring Strategist.

Your responsibility is to analyze the candidate's resume against the target job description and produce a high-quality tailoring strategy for the Resume Writer.

Your recommendations must ONLY be based on information already present or reasonably implied in the original resume.

Never recommend inventing:
- technologies
- skills
- certifications
- projects
- work experience
- metrics
- responsibilities

Focus on:

- Missing ATS keywords that can truthfully be incorporated
- Experiences that deserve more emphasis
- Skills that deserve better visibility
- Resume sections that should receive more attention

Resume:
{json.dumps(state["original_resume_json"])}

Job Description:
{json.dumps(state["job_description_json"])}

Return ONLY valid JSON in exactly this format:

{{
    "tailoring_plan":[
        "...",
        "...",
        "..."
    ],

    "ui_summary": {{
        "title":"Strategy Generated",
        "bullets":[
            "...",
            "...",
            "..."
        ]
    }}
}}

Rules for ui_summary:

- Maximum 3 bullets.
- Maximum 8 words each.
- Mention only the highest-impact strategy.
- Write them like progress updates for a user.
- Do NOT repeat the complete tailoring plan.
"""

    plan = await llm_for_agent("You are an expert career strategist.", prompt, json_mode = True)
    try:
        result = json.loads(plan)
    except:
        result = {
            "tailoring_plan": [],
            "ui_summary": {
                "title":"Strategy Generated",
                "bullets":["Unable to summarize"]
            }
        }

    return {"tailoring_plan": result["tailoring_plan"],
    "strategist_summary": result["ui_summary"]
    }



async def writer_node(state: tailor_state):
    # calling llm to rewrite the resume based on plan and previous feedback
    print("Writer is updating the resume")

    draft = state.get("current_draft_json") or state.get("original_resume_json")
    feedback = "\n".join(state.get("auditor_feedback", []))
    ats_report = state.get("ats_report", {})

    prompt = f"""
You are an expert Resume Writer.

Your task is to improve the resume while preserving complete factual accuracy.

If the Revision Plan conflicts with factual accuracy,
FACTUAL ACCURACY ALWAYS WINS.

Priority:

1. Follow the Revision Plan.
2. Preserve every factual statement.
3. Improve ATS relevance.
4. Align with the Job Description.
5. Preserve the exact JSON schema.
6. Never fabricate:
   - skills
   - technologies
   - certifications
   - metrics
   - projects
   - work experience

Revision Plan:
{json.dumps(state.get("revision_plan", {}))}

Current Resume:
{json.dumps(draft)}

Original Resume:
{json.dumps(state["original_resume_json"])}

Job Description:
{json.dumps(state["job_description_json"])}

Tailoring Plan:
{state["tailoring_plan"]}

Auditor Feedback:
{feedback}

ATS Report:
{json.dumps(ats_report)}

Return ONLY valid JSON.

Return exactly:

{{
    "resume": {{
        ...
    }},

    "ui_summary": {{
        "title":"Resume Updated",
        "bullets":[
            "...",
            "...",
            "..."
        ]
    }}
}}

Rules for ui_summary:

- Mention ONLY modifications actually performed.
- Never mention changes that were skipped.
- Maximum 3 bullets.
- Maximum 8 words each.
- Example bullets:
    - Summary rewritten
    - Skills reorganized
    - Experience refined
"""

    rewritten_str = await llm_for_agent("You are an expert resume writer. Output JSON only.", prompt, json_mode = True)
    try:
        rewritten_json = json.loads(rewritten_str)

        return {
            "current_draft_json": rewritten_json["resume"],
            "writer_summary": rewritten_json["ui_summary"]
        }

    except:
        return {
            "current_draft_json": draft,
            "writer_summary": {
                "title": "Resume Updated",
                "bullets": ["Writer output parsing failed"]
            }
        }


async def auditor_node(state: tailor_state):
    # calling llm to check if there are any hallucinations or not
    print("Auditor is checking for any hallucinations")

    prompt = f"""
You are a strict Resume Auditor.

Compare the Original Resume against the New Draft.

Your only job is to detect fabricated information.

Flag anything that was added but is NOT present or heavily implied in the Original Resume.

Examples:

- fake technologies
- fake metrics
- fake achievements
- fake certifications
- fake projects
- fake responsibilities

Original Resume:
{json.dumps(state["original_resume_json"])}

New Draft:
{json.dumps(state["current_draft_json"])}

Return ONLY valid JSON.

If everything is factually correct:

{{
    "status":"PASS",
    "feedback":[],
    "ui_summary":{{
        "title":"Fact Check Passed",
        "bullets":[
            "No hallucinations detected"
        ]
    }}
}}

Otherwise return:

{{
    "status":"FAIL",
    "feedback":[
        "...",
        "...",
        "..."
    ],

    "ui_summary":{{
        "title":"Hallucinations Found",
        "bullets":[
            "...",
            "...",
            "..."
        ]
    }}
}}

Rules:

- Feedback should be detailed.
- ui_summary should be concise.
- ui_summary bullets under 8 words.
"""

    auditor_result = await llm_for_agent("You are a strict fact-checker.", prompt, json_mode = True)
    print("=" * 50)
    print("AUDITOR RAW")
    print(type(auditor_result))
    print(repr(auditor_result))
    print("=" * 50)

    if auditor_result is None:
        raise Exception("LLM returned None")
        
    result = json.loads(auditor_result)

    
    if "PASS" in result["status"]:
        return {
    "auditor_feedback": [],
    "auditor_summary": result["ui_summary"]
}
    else:
        print(f"Auditor found something that should not be there in new draft: {result['feedback']}")
        return {
        "auditor_feedback": result["feedback"],
        "auditor_summary": result["ui_summary"]}


async def ats_evaluator_node(state: tailor_state):
    # calling llm to provide the ats score for current draft
    print("ATS evaluator is scoring the draft")

    prompt = f"""
You are an enterprise Applicant Tracking System.

Evaluate how well the resume matches the Job Description.

Evaluate:

- Keyword coverage
- Skills alignment
- Experience alignment
- Formatting
- ATS compatibility

Resume:
{json.dumps(state["current_draft_json"])}

Job Description:
{json.dumps(state["job_description_json"])}

Return ONLY valid JSON.

{{
    "overall_score":0,
    "keyword_match":0,
    "experience_match":0,
    "skills_match":0,
    "formatting_score":0,

    "missing_keywords":[],
    "missing_skills":[],

    "strengths":[],
    "weaknesses":[],
    "recommendations":[],

    "ui_summary":{{
        "title":"ATS Evaluation",
        "bullets":[
            "...",
            "...",
            "..."
        ]
    }}
}}

Rules for ui_summary:

- First bullet MUST mention ATS score.
- Second bullet should mention biggest weakness.
- Third bullet should mention highest-impact recommendation.
- Maximum 8 words per bullet.
"""

    ats_evaluator_result = await llm_for_agent("You are a strict ATS scoring engine", prompt, json_mode = True)
    try:
        evaluation = json.loads(ats_evaluator_result)
    except Exception:
        evaluation = {
            "overall_score": 0,
            "keyword_match": 0,
            "experience_match": 0,
            "skills_match": 0,
            "formatting_score": 0,
            "missing_keywords": [],
            "missing_skills": [],
            "strengths": [],
            "weaknesses": [],
            "recommendations": [],
            "ui_summary": {
        "title":"ATS Evaluation",
        "bullets":[
            "ATS unavailable"
        ]
    }
        }
    current_loops = state.get("loop_count", 0)
    return {
        "ats_score": evaluation["overall_score"],
        "ats_report": evaluation,
        "loop_count": current_loops + 1,
        "ats_evaluator_summary": evaluation["ui_summary"]
    }

async def revision_planner(state: tailor_state):
    print("Revision planner is writing planner for current draft")

    prompt = f"""
You are an expert Resume Revision Planner.

Your job is NOT to rewrite the resume.

Your job is to prepare the next revision strategy for the Resume Writer.

You must consider:

1. Original Tailoring Strategy
2. Current Resume
3. Original Resume
4. ATS Evaluation
5. Auditor Feedback
6. Job Description

Responsibilities:

- Preserve factual accuracy.
- Preserve useful tailoring recommendations.
- Fix every hallucination.
- Improve ATS score ONLY using truthful information.
- Ignore ATS suggestions that require inventing experience.
- Prioritize the highest-impact fixes.
- Avoid repeating already completed improvements.

Original Tailoring Strategy:
{state["tailoring_plan"]}

ATS Report:
{json.dumps(state.get("ats_report", {}))}

Auditor Feedback:
{json.dumps(state.get("auditor_feedback", []))}

Current Resume:
{json.dumps(state["current_draft_json"])}

Original Resume:
{json.dumps(state["original_resume_json"])}

Job Description:
{json.dumps(state["job_description_json"])}

Return ONLY valid JSON.

{{
    "priority_fixes":[...],
    "keyword_improvements":[...],
    "experience_improvements":[...],
    "skills_improvements":[...],
    "hallucination_fixes":[...],
    "final_writer_instructions":[...],

    "ui_summary":{{
        "title":"Revision Plan",
        "bullets":[
            "...",
            "...",
            "..."
        ]
    }}
}}

Rules for ui_summary:

- Mention ONLY the next highest-priority actions.
- Do not summarize the entire revision plan.
- Maximum 3 bullets.
- Maximum 8 words each.
"""

    revision_planner_result = await llm_for_agent("You are a strict Revision planning engine", prompt, json_mode = True)
    try:

        final_revision_planner_json = json.loads(revision_planner_result)
        return {
            "revision_plan": final_revision_planner_json,
            "revision_planner_summary": final_revision_planner_json["ui_summary"]
        }
    except:
        return {
            "revision_plan": "Revision Planner Generation Failed",
            "revision_planner_summary": "No summary generated as revision planner generation failed!"
        }

def should_continue(state: tailor_state):
    # checking if current draft is good enough or if it needs another rewrite loop
    if state["loop_count"] > 1:
        return END

    if state["ats_score"] < 80 or len(state["auditor_feedback"]) > 0:
        return "writer" # Send it back for revision

workflow = StateGraph(tailor_state)

# Add the nodes (Agents)
workflow.add_node("strategist", strategist_node)
workflow.add_node("writer", writer_node)
workflow.add_node("auditor", auditor_node)
workflow.add_node("ats_evaluator", ats_evaluator_node)
workflow.add_node("revision_planner", revision_planner)


# Define the edges (Flow)
workflow.set_entry_point("strategist")
workflow.add_edge("strategist", "writer")
workflow.add_edge("writer", "auditor")
workflow.add_edge("auditor", "ats_evaluator")
workflow.add_edge("ats_evaluator", "revision_planner")

# Conditional edge: After ATS evaluation, either finish or loop back to writer
workflow.add_conditional_edges(
    "revision_planner",
    should_continue,
    {
        "writer": "writer",
        END: END
    }
)

app = workflow.compile()

