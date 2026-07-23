from ai.llm import ask_ai
from ai.prompts import RESUME_CUSTOMIZATION_PROMPT
from utils.config import CANDIDATE_BACKGROUND


def customize_resume(master_resume, job_description):
    """Customizes a resume for a specific internship/job posting."""
    prompt = RESUME_CUSTOMIZATION_PROMPT.format(
        resume=master_resume,
        job_description=job_description,
        candidate_background=CANDIDATE_BACKGROUND,
    )
    return ask_ai(prompt)
