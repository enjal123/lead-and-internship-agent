from ai.llm import ask_ai
from ai.prompts import INTERNSHIP_ANALYSIS_PROMPT
from utils.config import CANDIDATE_BACKGROUND


def analyze_job(job_description):
    """Analyzes an internship posting to see whether the candidate is a fit."""
    prompt = INTERNSHIP_ANALYSIS_PROMPT.format(
        job_description=job_description,
        candidate_background=CANDIDATE_BACKGROUND,
    )
    return ask_ai(prompt)
