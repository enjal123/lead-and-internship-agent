import os
from datetime import datetime

from agents.resume_agent import customize_resume
from utils.file_manager import save_text
from utils.helpers import slugify
from utils.logger import logger

MASTER_RESUME_PATH = os.path.join(os.path.dirname(os.path.dirname(__file__)), "master_resume.txt")
GENERATED_DIR = os.path.join(os.path.dirname(os.path.dirname(__file__)), "generated")


def load_master_resume():
    if not os.path.exists(MASTER_RESUME_PATH):
        raise FileNotFoundError(f"Master resume not found at {MASTER_RESUME_PATH}.")

    with open(MASTER_RESUME_PATH, "r", encoding="utf-8") as f:
        content = f.read().strip()

    if not content:
        raise FileNotFoundError(
            f"{MASTER_RESUME_PATH} is empty. Paste your resume text into it before "
            "running the internship pipeline with resume building enabled."
        )

    return content


def build_resume_for_job(company, job_description):
    master_resume = load_master_resume()
    tailored_resume = customize_resume(master_resume, job_description)

    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    output_path = os.path.join(GENERATED_DIR, f"{slugify(company)}_{timestamp}.txt")

    save_text(output_path, tailored_resume)
    logger.info(f"Generated tailored resume: {output_path}")

    return output_path
