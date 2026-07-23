"""
A tiny helper to keep the agent from hammering any single site with
requests. Not a true token-bucket rate limiter -- just a polite,
configurable delay used between outbound requests.
"""
import time

from utils.config import REQUEST_DELAY_SECONDS


def polite_delay(seconds: float = None):
    """Sleep for REQUEST_DELAY_SECONDS (or an override) between requests."""
    time.sleep(seconds if seconds is not None else REQUEST_DELAY_SECONDS)
