from ai.llm import ask_ai
from ai.prompts import BUSINESS_ANALYSIS_PROMPT


def analyze_business(name, website):
    """Analyzes a business website to determine whether to engage them as a lead."""
    prompt = BUSINESS_ANALYSIS_PROMPT.format(
        business_name=name,
        website=website,
    )
    return ask_ai(prompt)
