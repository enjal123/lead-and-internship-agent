from ai.llm import ask_ai
from ai.prompts import LEAD_FILTERING_PROMPT


def qualify_lead(business_name, website, industry=None, website_issues=None):
    """Filters leads based on qualification and outreach fit."""
    prompt = LEAD_FILTERING_PROMPT.format(
        business_name=business_name,
        website=website,
        industry=industry or "Unknown",
        website_issues=website_issues or "Not provided",
    )
    return ask_ai(prompt)
