from scraper import scrape_jobs
from filter import filter_jobs
from storage import load_jobs, save_jobs, get_new_jobs
from notifier import send_jobs_email
from loguru import logger
from database import init_db

def main():
    logger.info("Starting Job Scraper with SQLite Storage...")

    init_db()

    # 1. Scrape jobs from the source
    scraped_jobs = scrape_jobs()
    logger.info(f"Scraped {len(scraped_jobs)} jobs total.")

    # 2. Filter jobs based on keywords
    logger.info("Filtering jobs based on Primary, Level, and Excluded keywords...")
    filtered_jobs = filter_jobs(scraped_jobs)
    logger.info(f"Found {len(filtered_jobs)} relevant jobs.")

    # 3. Identify new jobs that haven't been seen in the database yet
    new_jobs = get_new_jobs(filtered_jobs)
    logger.info(f"Identified {len(new_jobs)} brand new jobs.")

    # 4. Send new jobs via email
    if new_jobs:
        logger.info("Sending email with new jobs...")
        send_jobs_email(new_jobs)

        # 5. Save ONLY the new ones to the database to mark them as seen
        logger.info("Updating database with new jobs...")
        save_jobs(new_jobs)
    else:
        logger.info("No new jobs to notify.")

    logger.success("Job Scraper process complete.")

if __name__ == "__main__":
    main()