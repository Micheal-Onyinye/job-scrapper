from database import get_connection

def save_jobs(jobs):
    """Saves a list of jobs to the database. Ignores duplicates based on link."""
    conn = get_connection()
    cursor = conn.cursor()
    
    for job in jobs:
        try:
            cursor.execute("""
            INSERT OR IGNORE INTO jobs (title, company, link, source)
            VALUES (?, ?, ?, ?)
            """, (job['title'], job['company'], job['link'], job.get('source', 'Unknown')))
        except Exception as e:
            print(f"Error saving job {job['link']}: {e}")
            
    conn.commit()
    conn.close()

def load_jobs():
    """Loads all jobs from the database as a list of dictionaries."""
    conn = get_connection()
    cursor = conn.cursor()
    
    cursor.execute("SELECT title, company, link, source FROM jobs")
    rows = cursor.fetchall()
    
    jobs = [dict(row) for row in rows]
    
    conn.close()
    return jobs

def get_new_jobs(current_jobs):
    """
    Takes the freshly scraped jobs and checks which ones are NOT in the database yet.
    Returns only the truly new jobs.
    """
    conn = get_connection()
    cursor = conn.cursor()
    
    new_jobs = []
    for job in current_jobs:
        cursor.execute("SELECT 1 FROM jobs WHERE link = ?", (job['link'],))
        if cursor.fetchone() is None:
            new_jobs.append(job)
            
    conn.close()
    return new_jobs
