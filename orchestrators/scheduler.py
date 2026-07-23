"""
Simple periodic scheduler -- runs the business and internship pipelines
on an interval, without needing a separate cron job or task queue.

Run with: python -m orchestrators.scheduler
"""
import time

from orchestrators.business_pipeline import run_business_pipeline
from orchestrators.internship_pipeline import run_internship_pipeline
from utils.logger import logger

RUN_INTERVAL_SECONDS = 6 * 60 * 60  # every 6 hours


def run_scheduler():
    logger.info("Scheduler started. Running pipelines every "
                f"{RUN_INTERVAL_SECONDS // 3600} hours.")
    while True:
        try:
            run_business_pipeline()
            run_internship_pipeline()
        except Exception as e:
            logger.error(f"Scheduled run failed: {e}")

        time.sleep(RUN_INTERVAL_SECONDS)


if __name__ == "__main__":
    run_scheduler()
