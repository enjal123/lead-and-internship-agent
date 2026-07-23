"""
Sends email via SMTP (Gmail by default).

NOTE: the original version of this file read EMAIL_ADDRESS/EMAIL_PASSWORD
from the environment, but the project's .env file defined EMAIL/PASSWORD
instead -- so os.getenv() always returned None and every send silently
failed. Now sourced from utils.config, which matches .env.example.

For Gmail specifically, EMAIL_PASSWORD must be a 16-character App
Password (not your normal login password) -- see README for setup.
"""
import smtplib
from email.message import EmailMessage

from utils.config import EMAIL_ADDRESS, EMAIL_PASSWORD, SMTP_SERVER, SMTP_PORT
from utils.logger import logger


def send_email(recipient, subject, body):
    if not EMAIL_ADDRESS or not EMAIL_PASSWORD:
        raise RuntimeError(
            "EMAIL_ADDRESS / EMAIL_PASSWORD are not set. Add them to your "
            ".env file (see .env.example) before sending email."
        )

    message = EmailMessage()
    message["From"] = EMAIL_ADDRESS
    message["To"] = recipient
    message["Subject"] = subject
    message.set_content(body)

    with smtplib.SMTP_SSL(SMTP_SERVER, SMTP_PORT) as smtp:
        smtp.login(EMAIL_ADDRESS, EMAIL_PASSWORD)
        smtp.send_message(message)

    logger.info(f"Sent email to {recipient}: {subject}")
