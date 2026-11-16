@echo off
title MacTech iTool for Apple Devices
cd /d "%~dp0"

echo ========================================================
echo   MacTech iTool v2.5 (Universal Edition)
echo   Apple Forensic, Hardware Diagnostics & Revival Suite
echo   MacTech Solutions Lab
echo ========================================================
echo.

if exist "dist\MacTech_iTool.exe" (
    start "" "dist\MacTech_iTool.exe"
    exit /b
)

if exist "MacTech_iTool.exe" (
    start "" "MacTech_iTool.exe"
    exit /b
)

python main.py
if %ERRORLEVEL% NEQ 0 (
    echo.
    echo [!] Encountered an issue launching MacTech iTool.
    echo Running dependency verification...
    pip install -r requirements.txt
    python main.py
)
pause
