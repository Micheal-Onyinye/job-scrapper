#  Job Scraper & Auto Notifier

A professional, automated job scraping system that finds entry-level Python, Backend, and Automation roles, stores them in a local database, and sends daily email alerts.

##  Key Features

-   **Smart Scraping:** Uses Playwright (Headless Chrome) to handle modern, JavaScript-heavy job boards.
-   **Advanced Filtering:**
    -   **Primary Focus:** Python, Backend, Automation.
    -   **Entry-Level Focus:** Specifically targets Junior, Entry, Intern, and Associate roles.
    -   **Blacklist:** Automatically filters out Senior, Lead, and Manager roles.
-   **SQLite Database:** Professional data storage that prevents duplicate notifications and keeps the project folder clean.
-   **Performance Caching:** Saves website HTML locally for 60 minutes to prevent IP blocking and speed up debugging.
-   **Professional Logging:** Uses `loguru` to track success, warnings, and errors with timestamps.
-   **Windows Automation:** Fully integrated with Windows Task Scheduler for "set it and forget it" daily runs at 09:00 AM.

##  Project Structure

```text
job-scraper/
├── app/
│   ├── config.py         # Central settings (Keywords, Email, Paths)
│   ├── database.py       # SQLite connection and schema
│   ├── filter.py         # Smart logic for job matching/exclusion
│   ├── main.py           # Core execution flow
│   ├── notifier.py       # SMTP Email logic & HTML formatting
│   ├── scraper.py        # Playwright & BeautifulSoup logic
│   ├── storage.py        # Database CRUD operations
│   └── run_scraper.bat   # Launcher for Windows Task Scheduler
├── data/                 # Auto-created folder for DB and Cache
│   ├── jobs.db           # SQLite database
│   └── cache.html        # Temporary HTML cache
├── .env                  # Private credentials (Email/Password)
├── requirements.txt      # Python dependencies
└── README.md             # This guide
```

##  Installation

1.  **Clone the project** and navigate to the folder.
2.  **Create a Virtual Environment**:
    ```powershell
    python -m venv venv
    .\venv\Scripts\activate
    ```
3.  **Install Dependencies**:
    ```powershell
    pip install -r requirements.txt
    playwright install chromium
    ```
4.  **Configure `.env`**:
    Create a `.env` file in the root directory:
    ```env
    EMAIL_HOST=smtp.gmail.com
    EMAIL_PORT=587
    EMAIL_HOST_USER=your-email@gmail.com
    EMAIL_HOST_PASSWORD=your-app-password
    EMAIL_RECIPIENT=receiver-email@gmail.com
    ```

##  Usage

### Manual Run
To check for jobs immediately:
```powershell
.\venv\Scripts\python.exe app/main.py
```

### Automation (Windows Task Scheduler)
The project is configured to run at **09:00 AM daily**.

-   **To check task status:** `Get-ScheduledTask -TaskName "JobScraperDaily"`
-   **To run the task now:** `Start-ScheduledTask -TaskName "JobScraperDaily"`
-   **To stop/delete the task:** `Unregister-ScheduledTask -TaskName "JobScraperDaily"`

##  Configuration
You can customize the search by editing `app/config.py`:
-   `PRIMARY_KEYWORDS`: Skills you are looking for (e.g., Python).
-   `LEVEL_KEYWORDS`: Seniority levels (e.g., Junior).
-   `EXCLUDED_KEYWORDS`: Words to avoid (e.g., Senior).


