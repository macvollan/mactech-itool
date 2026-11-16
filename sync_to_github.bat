@echo off
title Sync MacTech iTool to GitHub
cd /d "%~dp0"
echo ========================================================
echo   Syncing MacTech iTool to GitHub
echo   Repository: macvollan/mactech-itool
echo ========================================================
python auto_sync_github.py %*
pause
