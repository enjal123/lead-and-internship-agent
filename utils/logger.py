"""
Shared application logger.

Logs INFO+ to the console, DEBUG+ to logs/app.log, and ERROR+ to
logs/errors.log so failures during long scraping/outreach runs are easy
to find after the fact.
"""
import logging
import os

LOG_DIR = "logs"
os.makedirs(LOG_DIR, exist_ok=True)

logger = logging.getLogger("ai_agent")
logger.setLevel(logging.DEBUG)

if not logger.handlers:
    formatter = logging.Formatter(
        "%(asctime)s | %(levelname)-8s | %(name)s | %(message)s"
    )

    console_handler = logging.StreamHandler()
    console_handler.setLevel(logging.INFO)
    console_handler.setFormatter(formatter)

    app_file_handler = logging.FileHandler(os.path.join(LOG_DIR, "app.log"))
    app_file_handler.setLevel(logging.DEBUG)
    app_file_handler.setFormatter(formatter)

    error_file_handler = logging.FileHandler(os.path.join(LOG_DIR, "errors.log"))
    error_file_handler.setLevel(logging.ERROR)
    error_file_handler.setFormatter(formatter)

    logger.addHandler(console_handler)
    logger.addHandler(app_file_handler)
    logger.addHandler(error_file_handler)
