import smtplib
import os
from dotenv import load_dotenv
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

from loguru import logger
from config import EMAIL_HOST, EMAIL_PORT, EMAIL_HOST_USER, EMAIL_HOST_PASSWORD, EMAIL_RECIPIENT

def send_email(subject, body):
    if not all([EMAIL_HOST, EMAIL_PORT, EMAIL_HOST_USER, EMAIL_HOST_PASSWORD, EMAIL_RECIPIENT]):
        logger.error("Email configuration is incomplete. Please check your .env file.")
        return

    msg = MIMEMultipart()
    msg["From"] = EMAIL_HOST_USER
    msg["To"] = EMAIL_RECIPIENT
    msg["Subject"] = subject

    msg.attach(MIMEText(body, "html"))

    try:
        with smtplib.SMTP(EMAIL_HOST, EMAIL_PORT) as server:
            server.starttls()
            server.login(EMAIL_HOST_USER, EMAIL_HOST_PASSWORD)
            server.send_message(msg)
        logger.info("Email sent successfully!")
    except Exception as e:
        logger.error(f"Failed to send email: {e}")

def format_job_html(job):
    return f"""
    <div style="margin-bottom: 20px; padding: 10px; border: 1px solid #ddd; border-radius: 5px;">
        <h3 style="margin: 0 0 10px 0;">{job['title'].title()}</h3>
        <p style="margin: 0 0 5px 0;"><strong>Company:</strong> {job['company'].title()}</p>
        <p style="margin: 0 0 5px 0;"><strong>Source:</strong> {job.get('source', 'Unknown')}</p>
        <a href="{job['link']}" style="color: #007bff; text-decoration: none;">View Job</a>
    </div>
    """

def send_jobs_email(jobs):
    if not jobs:
        logger.info("No new jobs to send in email.")
        return

    subject = f"Job Scraper: {len(jobs)} New Job Alerts"
    
    html = "<h1> New Job Alerts </h1>"
    for job in jobs:
        html += format_job_html(job)

    send_email(subject, html)
