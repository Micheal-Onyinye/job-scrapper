@echo off

SET BASE_DIR=%~dp0
cd /d %BASE_DIR%

..\venv\Scripts\python.exe main.py

echo Scraper finished at %date% %time% >> ..\data\run_log.txt
