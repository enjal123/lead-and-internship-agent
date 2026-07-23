from ai.llm import ask_ai
from ai.prompts import BUSINESS_RESEARCH_PROMPT


def research_business(business_name, website, description):
    """Researches business context and outreach angles."""
    prompt = BUSINESS_RESEARCH_PROMPT.format(
        business_name=business_name,
        website=website,
        description=description,
    )
    return ask_ai(prompt)
