"""
Central configuration for the AI Outreach Agent.

Every value is loaded from environment variables (see .env.example) so
that no secrets or personal settings are ever hardcoded in the codebase.
"""
import os
from dotenv import load_dotenv

load_dotenv()


def _bool(value, default=False):
    if value is None:
        return default
    return value.strip().lower() in ("1", "true", "yes", "on")


# --- LLM (local, free via Ollama) ---
OLLAMA_MODEL = os.getenv("OLLAMA_MODEL", "llama3")

# --- Browser / scraping ---
HEADLESS_BROWSER = _bool(os.getenv("HEADLESS_BROWSER"), default=True)
REQUEST_TIMEOUT = int(os.getenv("REQUEST_TIMEOUT", "10"))
REQUEST_DELAY_SECONDS = float(os.getenv("REQUEST_DELAY_SECONDS", "2"))
USER_AGENT = (
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
    "AppleWebKit/537.36 (KHTML, like Gecko) "
    "Chrome/122.0.0.0 Safari/537.36"
)

# --- Email / SMTP ---
EMAIL_ADDRESS = os.getenv("EMAIL_ADDRESS")
EMAIL_PASSWORD = os.getenv("EMAIL_PASSWORD")
SMTP_SERVER = os.getenv("SMTP_SERVER", "smtp.gmail.com")
SMTP_PORT = int(os.getenv("SMTP_PORT", "465"))
YOUR_NAME = os.getenv("YOUR_NAME", "Your Name")

# --- Database ---
DATABASE_PATH = os.getenv("DATABASE_PATH", "agent.db")

# --- Optional paid geocoding / places API (NOT required to run the agent) ---
# Left as an opt-in extension point. If unset, business discovery falls back
# to the free, no-key DuckDuckGo search path instead.
GOOGLE_PLACES_API_KEY = os.getenv("GOOGLE_PLACES_API_KEY", "")

# --- Candidate/sender background injected into prompts ---
# Override this in .env with your own background so the AI agents write
# in a way that's accurate for you. Kept generic here for a public repo.
CANDIDATE_BACKGROUND = os.getenv(
    "CANDIDATE_BACKGROUND",
    "- early-career software engineering student\n"
    "- self-taught programming background\n"
    "- proficient in Python\n"
    "- proficient in HTML/CSS/JavaScript\n"
    "- familiar with SQL\n"
    "- proficient with Git/GitHub\n"
    "- comfortable using AI tools and workflows\n"
    "- has built and shipped independent projects",
)

SENDER_BACKGROUND = os.getenv(
    "SENDER_BACKGROUND",
    "- a student software developer\n"
    "- builds websites completely from scratch\n"
    "- uses HTML, CSS, JavaScript, React, and modern technologies\n"
    "- does NOT use templates or website builders\n"
    "- specializes in custom websites\n"
    "- understands SEO, performance, and responsive design\n"
    "- has worked with local businesses before",
)

# --- Default search queries (override in .env or pass explicitly) ---
INTERNSHIP_SEARCH_QUERY = os.getenv(
    "INTERNSHIP_SEARCH_QUERY", "software engineering internship 2026 apply"
)
BUSINESS_SEARCH_QUERY = os.getenv(
    "BUSINESS_SEARCH_QUERY", "small business website Sonoma County California"
)
