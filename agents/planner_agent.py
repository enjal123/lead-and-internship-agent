from ai.llm import ask_ai
from ai.prompts import OUTREACH_PLANNER_PROMPT


def create_outreach_plan(business_name, website, business_overview):
    """Creates a step-by-step outreach plan for a lead."""
    prompt = OUTREACH_PLANNER_PROMPT.format(
        business_name=business_name,
        website=website,
        business_overview=business_overview,
    )
    return ask_ai(prompt)
