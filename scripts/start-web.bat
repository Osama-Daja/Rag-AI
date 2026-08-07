@echo off
setlocal
title Rag-AI Web

cd /d "%~dp0..\apps\web"

where npm >nul 2>&1
if errorlevel 1 (
  echo [ERROR] npm is not on PATH. Install Node.js and try again.
  exit /b 1
)

if not exist "node_modules" (
  echo Installing npm dependencies...
  call npm install
  if errorlevel 1 (
    echo [ERROR] npm install failed.
    exit /b 1
  )
)

if not exist ".env.local" (
  if exist ".env.example" (
    copy /Y ".env.example" ".env.local" >nul
    echo Created .env.local from .env.example
  )
)

echo Starting Next.js on http://localhost:3000
call npm run dev

endlocal
