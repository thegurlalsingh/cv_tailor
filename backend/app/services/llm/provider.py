from langchain_core.messages import content
from openai.resources import responses
from openai import AsyncOpenAI
from app.core.config import settings
import json

model_name = "inclusionai/ling-3.0-flash:free"

client = AsyncOpenAI(
    base_url = "https://openrouter.ai/api/v1",
    api_key = settings.api_key_llm
)

# Takes raw extracted PDF text and uses OpenRouter to convert it into structured JSON.
async def structured_resume_text(raw_text: str) -> dict:
    prompt = f"""
    You are an expert resume parser. Extract the following raw resume text into a structured JSON format.
    Return ONLY valid JSON.

    Rules:
    - NEVER invent information.
    - NEVER infer missing information.
    - If a field is missing, use "" or [].
    - Copy values exactly from the resume.
    - If uncertain, leave the field empty.
    - Return ONLY valid JSON.
    
    Required JSON structure:
    {{
        "personal_info": {{...}},
        "summary": "...",

        "education": [...],

        "experience": [...],

        "projects": [...],

        "publications": [...],

        "leadership": [...],

        "skills": {{
            "languages": [],
            "frontend": [],
            "backend": [],
            "databases": [],
            "ai_ml": [],
            "tools": [],
            "concepts": []
        }},

        "achievements": []
    }}
    Raw Resume Text:
    {raw_text}
    """

    try:
        response = await client.chat.completions.create(
            model = model_name,
            messages = [
                {"role": "system", "content": "You are a helpful AI that strictly outputs valid JSON."},
                {"role": "user", "content": prompt}
            ],
            # response_format = {
            #     "type": "json_object"
            # },
            temperature = 0.1,
        )
        print("RAW RESPONSE")
        print(response)

        content = response.choices[0].message.content

        if not content:
            raise ValueError("LLM returned empty content")

        content = response.choices[0].message.content

        if content is None:
            raise Exception(f"Model returned None.\nFull response:\n{response}")

        if content.startswith("```"):
            lines = content.splitlines()

            if lines[0].startswith("```"):
                lines = lines[1:]

            if lines and lines[-1].startswith("```"):
                lines = lines[:-1]

            content = "\n".join(lines).strip()
        
        print("===============================")
        print("CONTENT FOR RESUME TEXT")
        print(content)

        return content
    
    except Exception as e:
        print(f"LLM Parsing error: {e}")
        return {
            "error": str(e)
        }


async def structured_jd_text(raw_text: str) -> dict:
    prompt = f"""
    Extract the following job description into a structured JSON format.
    Return ONLY valid JSON.
    
    Required JSON structure:
    {{
        "job_title": "",
        "company": "",
        "must_have_skills": ["...", "..."],
        "nice_to_have_skills": ["...", "..."],
        "key_responsibilities": ["...", "..."]
    }}
    
    Job Description Text:
    {raw_text}
    """

    try:
        response = await client.chat.completions.create(
            model = model_name,
            messages = [
                {"role": "system", "content": "You are a helpful AI that strictly outputs valid JSON."},
                {"role": "user", "content": prompt}
            ],
            # response_format = {
            #     "type": "json_object"
            # },
            temperature = 0.1,
        )

        # print("RAW RESPONSE")
        # print(response)

        content = response.choices[0].message.content

        if not content:
            raise ValueError("LLM returned empty content")

        content = response.choices[0].message.content

        if content is None:
            raise Exception(f"Model returned None.\nFull response:\n{response}")

        if content.startswith("```"):
            lines = content.splitlines()

            if lines[0].startswith("```"):
                lines = lines[1:]

            if lines and lines[-1].startswith("```"):
                lines = lines[:-1]

            content = "\n".join(lines).strip()

        print("===============================")
        print("CONTENT FOR JD TEXT")
        print(content)

        return content
    
    except Exception as e:
        print(f"LLM Parsing error: {e}")
        return {
            "error": str(e)
        }


async def llm_for_agent(system_prompt: str, user_prompt: str, json_mode: bool = False) -> str:
    try:
        kwargs = {
            "model": model_name,
            "messages": [
                {
                    "role":"system",
                    "content": system_prompt + "\nAlways output valid JSON."
                },
                {
                    "role":"user",
                    "content": user_prompt
                }
            ],
            "temperature": 0.1
        }

        if json_mode:
            kwargs = {
                "model": model_name,
                "messages": [
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": user_prompt},
                ],
                "temperature": 0.1,
            }

            # Only for models that support it
        if json_mode and model_name in [
                "google/gemma-4-31b",
                "openai/gpt-oss-20b:free",
            ]:
                kwargs["response_format"] = {
                    "type": "json_object"
                }

        response = await client.chat.completions.create(**kwargs)
        content = response.choices[0].message.content

        if content is None:
            raise Exception(f"Model returned None.\nFull response:\n{response}")

        if content.startswith("```"):
            lines = content.splitlines()

            if lines[0].startswith("```"):
                lines = lines[1:]

            if lines and lines[-1].startswith("```"):
                lines = lines[:-1]

            content = "\n".join(lines).strip()

        print("===============================")
        print("CONTENT FOR AGENT")
        print(content)

        return content
    
    except Exception as e:
        print(f"LLM error: {e}")
        raise