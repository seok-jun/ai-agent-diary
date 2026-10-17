@echo off
setlocal
chcp 65001 >nul
cd /d "%~dp0"
powershell.exe -NoProfile -ExecutionPolicy Bypass -File "%~dp0_meta\activity\one-click.ps1" -Setup
echo.
pause
exit /b %ERRORLEVEL%
