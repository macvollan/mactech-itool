@echo off
title MacTech iTool - Windows Environment & Driver Setup
cd /d "%~dp0"

echo ==============================================================================
echo   MacTech iTool - Windows 1-Step Environment & Apple Driver Setup
echo   MacTech Solutions Lab - https://mactechsolutionslab.vercel.app
echo ==============================================================================
echo.

echo [1/3] Verifying Python and installing required packages...
python -m pip install --upgrade pip
python -m pip install -r requirements.txt
if %ERRORLEVEL% NEQ 0 (
    echo [!] Warning: Pip install returned a non-zero exit code.
) else (
    echo [OK] Python dependencies verified.
)

echo.
echo [2/3] Checking Apple Mobile Device Support (AMDS) & Drivers...
sc query "Apple Mobile Device Service" | find "RUNNING" >nul
if %ERRORLEVEL% EQU 0 (
    echo [OK] Apple Mobile Device Service is RUNNING on Port 27015!
) else (
    sc query "Apple Mobile Device Service" >nul 2>&1
    if %ERRORLEVEL% EQU 0 (
        echo [*] Starting Apple Mobile Device Service...
        net start "Apple Mobile Device Service"
    ) else (
        echo [!] Apple Mobile Device Support (AMDS) is not installed on this PC.
        echo [*] MacTech iTool requires the official 64-bit Apple drivers to communicate
        echo     with iOS/iPadOS hardware over USB.
        echo.
        echo [?] Would you like to open the official Apple 64-bit driver download?
        choice /C YN /M "Open Apple Driver Download now"
        if errorlevel 1 if not errorlevel 2 (
            start https://secure-appldnld.apple.com/itunes12/001-44813-20200520-3B1D46CE-9AB2-11EA-9B7C-A8E9A348B47E/iTunes64Setup.exe
        )
    )
)

echo.
echo [3/3] Checking Apple USB Driver (usbaapl64.sys)...
if exist "C:\Windows\System32\drivers\usbaapl64.sys" (
    echo [OK] Apple Lightning / USB-C Kernel Driver (usbaapl64.sys) is present.
) else (
    echo [i] Apple USB driver will be registered upon AMDS installation.
)

echo.
echo ==============================================================================
echo   Windows Environment Setup Complete!
echo   You can now run Launch_Tool.bat or python main.py
echo ==============================================================================
pause
