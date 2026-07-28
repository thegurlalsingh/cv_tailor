from weasyprint import HTML
from jinja2 import Environment, FileSystemLoader
import os

TEMPLATE_DIR = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(__file__))), "templates")
env = Environment(loader = FileSystemLoader(TEMPLATE_DIR))

def generate_pdf_from_json(resume_json: dict, output_path: str) -> str:
    template = env.get_template("resume_template.html")

    
    html_out = template.render(
        personal_info=resume_json.get("personal_info", {}),
        summary=resume_json.get("summary", ""),
        education=resume_json.get("education", []),
        experience=resume_json.get("experience", []),
        publications=resume_json.get("publications", []),
        projects=resume_json.get("projects", []),
        leadership=resume_json.get("leadership", []),
        skills=resume_json.get("skills", {}),
        achievements=resume_json.get("achievements", [])
    )
   
    options = {
        "page-size": "A4",
        "margin-top": "0.5in",
        "margin-right": "0.5in",
        "margin-bottom": "0.5in",
        "margin-left": "0.5in",
        "encoding": "UTF-8",
        "enable-local-file-access": None,
        "print-media-type": None,
        "disable-smart-shrinking": None,
        "no-outline": None,
    }

    HTML(string = html_out).write_pdf(output_path)

    return output_path