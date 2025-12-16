"""Configuration module for loading environment variables."""
import os
from dotenv import load_dotenv

load_dotenv()

BEARER_TOKEN: str = os.getenv("BEARER_TOKEN", "")
if not BEARER_TOKEN:
    raise ValueError("BEARER_TOKEN environment variable is required")

