@echo off
setlocal
chcp 65001 >nul
cd /d "%~dp0"
set "ARGS="
if /I "%~1"=="--scheduled" set "ARGS=-Scheduled"
powershell.exe -NoProfile -ExecutionPolicy RemoteSigned -File "%~dp0_meta\activity\one-click.ps1" %ARGS%
set "RESULT=%ERRORLEVEL%"
if "%RESULT%"=="0" (
  echo.
  echo Activity update finished.
) else (
  echo.
  echo Activity update failed. No partial update was published.
)
if /I not "%~1"=="--scheduled" pause
exit /b %RESULT%
