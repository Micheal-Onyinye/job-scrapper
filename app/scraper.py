from bs4 import BeautifulSoup
from playwright.sync_api import sync_playwright
import re
import os
import time
from loguru import logger
from config import CACHE_FILE, CACHE_EXPIRY_MINUTES

# ---------------------------
# Caching logic
# ---------------------------
def get_cached_html():
    if not os.path.exists(CACHE_FILE):
        return None

    file_age_seconds = time.time() - os.path.getmtime(CACHE_FILE)
    if file_age_seconds > (CACHE_EXPIRY_MINUTES * 60):
        logger.info(f"Cache expired ({int(file_age_seconds/60)} mins old).")
        return None

    logger.info(f"Using cached HTML ({int(file_age_seconds/60)} mins old).")
    with open(CACHE_FILE, "r", encoding="utf-8") as f:
        return f.read()

def save_cache(html):
    with open(CACHE_FILE, "w", encoding="utf-8") as f:
        f.write(html)
    logger.info("HTML saved to cache.")

# ---------------------------
# Convert relative date → days
# ---------------------------
def convert_to_days(job_date):
    if not job_date:
        return 999

    job_date = job_date.lower()
    if "d" in job_date:
        match = re.search(r'\d+', job_date)
        return int(match.group()) if match else 1
    elif "w" in job_date:
        match = re.search(r'\d+', job_date)
        return int(match.group()) * 7 if match else 7
    elif "h" in job_date:
        return 0
    elif "mo" in job_date:
        match = re.search(r'\d+', job_date)
        return int(match.group()) * 30 if match else 30
    else:
        return 999


# ---------------------------
# Clean job data
# ---------------------------
def clean_job(title, company, link, job_date):

    if not title or not link:
        return None

    title = title.strip().lower()
    company = company.strip().lower() if company else "unknown"
    link = link.strip()
    job_date = job_date.strip() if job_date else "unknown"

    return {
        "title": title,
        "company": company,
        "link": link,
        "date": job_date
    }


def standardize_job(job):
    return {
        "title": job.get("title", "").lower().strip(),
        "company": job.get("company", "unknown").lower().strip(),
        "link": job.get("link", "").strip(),
        "source": "RemoteOK"
    }

def remove_duplicates(jobs):
    seen = set()
    unique_jobs = []

    for job in jobs:
        if job["link"] not in seen:
            seen.add(job["link"])
            unique_jobs.append(job)

    return unique_jobs

# ---------------------------
# Main scraper
# ---------------------------
def scrape_jobs():
    url = "https://remoteok.com/remote-python-jobs"
    jobs = []

    html_content = get_cached_html()

    if not html_content:
        logger.info(f"Fetching fresh data from {url}...")
        try:
            with sync_playwright() as p:
                browser = p.chromium.launch(headless=True)
                page = browser.new_page(user_agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.0.0 Safari/537.36")
                page.goto(url, wait_until="networkidle")

                logger.info(f"Page loaded: {page.title()}")

                # Wait for any table or specific job markers
                try:
                    page.wait_for_selector("tr.job", timeout=10000)
                except:
                    logger.warning("Specific job selector not found, attempting to capture HTML anyway.")

                html_content = page.content()
                browser.close()
                save_cache(html_content)
        except Exception as e:
            logger.error(f"Playwright error: {e}")
            return jobs
    soup = BeautifulSoup(html_content, "html.parser")
    # RemoteOK sometimes uses id="jobsboard" or class="jobsboard"
    table = soup.find("table", id="jobsboard") or soup.find("table", class_="jobsboard")

    if not table:
        logger.warning("No job table found in HTML.")
        return jobs

    rows = table.find_all("tr", attrs={"data-id": True})

    for row in rows:
        try:
            if "sponsored" in row.get("class", []) or not row.find("h2"):
                continue

            title_tag = row.find("h2")
            company_tag = row.find("h3")
            link_tag = row.find("a", href=True)
            date_tag = row.find("time")

            if not title_tag or not link_tag:
                continue

            title = title_tag.text
            company = company_tag.text if company_tag else ""
            link = "https://remoteok.com" + link_tag["href"]
            job_date = date_tag.text if date_tag else ""

            job = clean_job(title, company, link, job_date)
            if job is None:
                continue

            days = convert_to_days(job["date"])
            if days > 30:
                continue

            job = standardize_job(job)
            jobs.append(job)

        except Exception as e:
            logger.error(f"Error parsing job row: {e}")
            continue

    jobs = remove_duplicates(jobs)
    logger.info(f"Successfully scraped {len(jobs)} unique jobs from RemoteOK.")

    return jobs