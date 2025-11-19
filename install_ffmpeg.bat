@echo off
echo ============================================
echo FFmpeg Installation Script for Windows
echo ============================================
echo.
echo This script will attempt to install FFmpeg using winget.
echo.
echo Checking if winget is available...
where winget >nul 2>nul
if %ERRORLEVEL% NEQ 0 (
    echo ERROR: winget is not available on your system.
    echo.
    echo Please install FFmpeg manually:
    echo 1. Download from: https://www.gyan.dev/ffmpeg/builds/
    echo 2. Extract the archive
    echo 3. Add the bin folder to your PATH
    echo.
    pause
    exit /b 1
)

echo winget found! Installing FFmpeg...
echo.
winget install ffmpeg

if %ERRORLEVEL% EQU 0 (
    echo.
    echo ============================================
    echo FFmpeg installed successfully!
    echo ============================================
    echo.
    echo Please restart your terminal or command prompt
    echo for the changes to take effect.
    echo.
    echo You can verify the installation by running:
    echo   ffmpeg -version
    echo.
) else (
    echo.
    echo ============================================
    echo Installation failed!
    echo ============================================
    echo.
    echo Please try installing manually:
    echo 1. Download from: https://www.gyan.dev/ffmpeg/builds/
    echo 2. Extract the archive
    echo 3. Add the bin folder to your PATH
    echo.
)

pause

