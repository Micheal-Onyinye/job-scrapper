import os
from dotenv import load_dotenv

load_dotenv()

# Email Configuration
EMAIL_HOST = os.getenv("EMAIL_HOST", "smtp.gmail.com")
EMAIL_PORT = int(os.getenv("EMAIL_PORT", 587))
EMAIL_HOST_USER = os.getenv("EMAIL_HOST_USER")
EMAIL_HOST_PASSWORD = os.getenv("EMAIL_HOST_PASSWORD")
EMAIL_RECIPIENT = os.getenv("EMAIL_RECIPIENT")

CACHE_EXPIRY_MINUTES = int(os.getenv("CACHE_EXPIRY_MINUTES", 60))

PRIMARY_KEYWORDS = ["python", "backend", "automation"]

LEVEL_KEYWORDS = ["junior", "entry", "intern", "associate", "graduate"]

EXCLUDED_KEYWORDS = ["senior", "lead", "staff", "principal", "manager", "sr", "director", "architect"]

KEYWORDS = PRIMARY_KEYWORDS + LEVEL_KEYWORDS


BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DATA_DIR = os.path.join(os.path.dirname(BASE_DIR), "data")

if not os.path.exists(DATA_DIR):
    os.makedirs(DATA_DIR)

JOBS_STORAGE_FILE = os.path.join(DATA_DIR, "jobs.json")
CACHE_FILE = os.path.join(DATA_DIR, "cache.html")
