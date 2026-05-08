import schedule
import time
from loguru import logger
from main import main as job_scraper_task

def start_scheduler():
    logger.info("Scheduler started. Running job scraper every day at 09:00.")
    
    # Schedule the job to run every day at 9:00 AM
    schedule.every().day.at("09:00").do(job_scraper_task)
    
    # Run once immediately on start for testing
    logger.info("Running initial scrape...")
    job_scraper_task()

    while True:
        schedule.run_pending()
        time.sleep(60)

if __name__ == "__main__":
    try:
        start_scheduler()
    except KeyboardInterrupt:
        logger.info("Scheduler stopped by user.")
    except Exception as e:
        logger.error(f"Scheduler error: {e}")
