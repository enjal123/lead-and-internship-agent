import re

from ai.llm import ask_ai
from ai.prompts import LEAD_SCORING_PROMPT
from utils.logger import logger


def score_lead(ai_analysis):
    """
    Asks the LLM to score a lead 1-10 and parses out the integer.

    LLMs don't always return a bare integer even when asked to, so this
    pulls the first number out of the response instead of assuming
    `int(response.strip())` will always succeed.
    """
    prompt = LEAD_SCORING_PROMPT.format(ai_analysis=ai_analysis)
    response = ask_ai(prompt).strip()

    match = re.search(r"\d+", response)
    if not match:
        logger.error(f"Could not parse a lead score from LLM response: {response!r}")
        return 0

    return int(match.group())
