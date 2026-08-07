@echo off
setlocal
title Rag-AI API

cd /d "%~dp0..\apps\api"

set "PY="
where py >nul 2>&1
if not errorlevel 1 (
  for %%V in (3.12 3.11 3.13 3.14 3) do (
    if not defined PY (
      py -%%V -c "import venv" >nul 2>&1
      if not errorlevel 1 set "PY=py -%%V"
    )
  )
)

if not defined PY (
  where python >nul 2>&1
  if not errorlevel 1 (
    python -c "import venv" >nul 2>&1
    if not errorlevel 1 set "PY=python"
  )
)

if not defined PY (
  echo [ERROR] No Python with venv found. Install Python 3.11+ from python.org
  echo         Tip: use "py -3.12" / Python 3.11+ full installer, not embeddable.
  exit /b 1
)

echo Using: %PY%

if not exist ".venv\Scripts\python.exe" (
  echo Creating virtual environment...
  %PY% -m venv .venv
  if errorlevel 1 (
    echo [ERROR] Failed to create .venv
    exit /b 1
  )
)

call ".venv\Scripts\activate.bat"
echo Installing Python dependencies...
python -m pip install --upgrade pip
python -m pip install -r requirements.txt
if errorlevel 1 (
  echo [ERROR] pip install failed.
  exit /b 1
)

if not exist ".env" (
  if exist ".env.example" (
    copy /Y ".env.example" ".env" >nul
    echo Created .env from .env.example
  )
)

REM Prefer project .env values over leftover machine env vars
for /f "usebackq eol=# tokens=1,* delims==" %%A in (".env") do (
  if not "%%A"=="" set "%%A=%%B"
)

echo Starting FastAPI on http://localhost:8000
echo Docs: http://localhost:8000/docs
echo Qdrant collection: %QDRANT_COLLECTION%
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000

endlocal
