@echo off
setlocal
set "ROOT=%~dp0.."
set "PY=%ROOT%\.venv\Scripts\python.exe"
if not exist "%PY%" (
  echo Missing local DynaCPI virtual environment: "%PY%"
  echo See demo_app\README.md for setup requirements.
  pause
  exit /b 1
)
powershell -NoProfile -Command "try { $null=Invoke-WebRequest -UseBasicParsing 'http://127.0.0.1:8765/api/health' -TimeoutSec 2; exit 0 } catch { exit 1 }" >nul 2>&1
if errorlevel 1 (
  echo Starting DynaCPI demo server...
  start "DynaCPI Demo Server" "%PY%" "%~dp0server.py"
  timeout /t 4 /nobreak >nul
) else (
  echo Demo server already running.
)
start "" "http://127.0.0.1:8765/"
echo Opened DynaCPI demo in your browser.
exit /b 0
