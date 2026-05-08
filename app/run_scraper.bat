@echo off
:: Get the directory of the current batch script
SET BASE_DIR=%~dp0
cd /d %BASE_DIR%

:: Run the scraper using the virtual environment's python
..\venv\Scripts\python.exe main.py

:: Log the completion time (optional but helpful)
echo Scraper finished at %date% %time% >> ..\data\run_log.txt
