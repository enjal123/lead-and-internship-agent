from ai.llm import ask_ai
from ai.prompts import OUTREACH_EMAIL_PROMPT
from utils.config import SENDER_BACKGROUND


def generate_outreach(business_name, website="Unknown", business_type="Unknown", website_issues="Not provided"):
    """
    Generates a cold outreach email for a business lead.

    NOTE: the original version of this function only passed
    `business_name` into OUTREACH_EMAIL_PROMPT.format(...), but the
    template also requires business_type, website, and website_issues --
    calling it with only one argument raised a KeyError every time.
    """
    prompt = OUTREACH_EMAIL_PROMPT.format(
        sender_background=SENDER_BACKGROUND,
        business_name=business_name,
        business_type=business_type,
        website=website,
        website_issues=website_issues,
    )
    return ask_ai(prompt)
