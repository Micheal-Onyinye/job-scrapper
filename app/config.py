import os
from dotenv import load_dotenv

load_dotenv()

# Email Configuration
EMAIL_HOST = os.getenv("EMAIL_HOST", "smtp.gmail.com")
EMAIL_PORT = int(os.getenv("EMAIL_PORT", 587))
EMAIL_HOST_USER = os.getenv("EMAIL_HOST_USER")
EMAIL_HOST_PASSWORD = os.getenv("EMAIL_HOST_PASSWORD")
EMAIL_RECIPIENT = os.getenv("EMAIL_RECIPIENT")

# Scraper Configuration
CACHE_EXPIRY_MINUTES = int(os.getenv("CACHE_EXPIRY_MINUTES", 60))

# The bot will look for jobs containing ANY of these primary focuses
PRIMARY_KEYWORDS = ["python", "backend", "automation"]

# The bot will prioritize or require these level-based keywords
LEVEL_KEYWORDS = ["junior", "entry", "intern", "associate", "graduate"]

# The bot will EXCLUDE any job containing these words
EXCLUDED_KEYWORDS = ["senior", "lead", "staff", "principal", "manager", "sr", "director", "architect"]

# Combined list for legacy support in main.py if needed
KEYWORDS = PRIMARY_KEYWORDS + LEVEL_KEYWORDS

# File Paths
# Use absolute path for DATA_DIR to avoid relative path issues
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DATA_DIR = os.path.join(os.path.dirname(BASE_DIR), "data")

# Create data directory if it doesn't exist
if not os.path.exists(DATA_DIR):
    os.makedirs(DATA_DIR)

JOBS_STORAGE_FILE = os.path.join(DATA_DIR, "jobs.json")
CACHE_FILE = os.path.join(DATA_DIR, "cache.html")
