from ai.llm import ask_ai
from ai.prompts import IS_GOOD_LEAD_PROMPT, FRESHMAN_FRIENDLY_PROMPT
from utils.config import CANDIDATE_BACKGROUND


def is_good_lead(business_name, website_issues):
    prompt = IS_GOOD_LEAD_PROMPT.format(
        business_name=business_name,
        website_issues=website_issues,
    )
    return ask_ai(prompt).upper()


def is_freshman_friendly(job_description):
    prompt = FRESHMAN_FRIENDLY_PROMPT.format(
        job_description=job_description,
        candidate_background=CANDIDATE_BACKGROUND,
    )
    response = ask_ai(prompt)
    return "YES" in response.upper()
