@echo off
setlocal
title Rag-AI Qdrant

cd /d "%~dp0.."

where docker >nul 2>&1
if errorlevel 1 (
  echo [ERROR] Docker is not on PATH. Install Docker Desktop and try again.
  exit /b 1
)

echo Starting Qdrant...
docker compose -f docker\docker-compose.yml up -d
if errorlevel 1 (
  echo [ERROR] Failed to start Qdrant.
  exit /b 1
)

echo Qdrant is up at http://localhost:6333
endlocal
