@echo off
setlocal
title Rag-AI Stop Qdrant

cd /d "%~dp0.."

where docker >nul 2>&1
if errorlevel 1 (
  echo [ERROR] Docker is not on PATH. Install Docker Desktop and try again.
  exit /b 1
)

echo Stopping Qdrant...
docker compose -f docker\docker-compose.yml down
if errorlevel 1 (
  echo [ERROR] Failed to stop Qdrant.
  exit /b 1
)

echo Qdrant stopped.
endlocal
