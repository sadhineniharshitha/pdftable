@echo off
REM Download and setup Poppler for Windows
REM This script downloads poppler-windows and configures it

setlocal enabledelayedexpansion

echo Downloading Poppler for Windows...
echo This may take a few minutes...

REM Download the latest poppler-windows release
powershell -Command "(New-Object System.Net.ServicePointManager).SecurityProtocol = [System.Net.SecurityProtocolType]::Tls12; Invoke-WebRequest -Uri 'https://github.com/oschwartz10612/poppler-windows/releases/download/v24.08.0/Release-24.08.0.zip' -OutFile '%USERPROFILE%\AppData\Local\Temp\poppler.zip' -UseBasicParsing"

if %ERRORLEVEL% neq 0 (
    echo Error downloading poppler. Please download manually from:
    echo https://github.com/oschwartz10612/poppler-windows/releases/
    echo Extract to: C:\poppler
    pause
    exit /b 1
)

echo Extracting Poppler...
powershell -Command "Expand-Archive -Path '%USERPROFILE%\AppData\Local\Temp\poppler.zip' -DestinationPath '%USERPROFILE%\AppData\Local\' -Force"

echo Setting up PATH environment variable...
setx PATH "%USERPROFILE%\AppData\Local\Release-24.08.0\Library\bin;!PATH!"

echo.
echo ✓ Poppler installed successfully!
echo Please restart your Flask application.
echo.
pause
