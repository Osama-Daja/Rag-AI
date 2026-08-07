@echo off
setlocal
title Rag-AI Start All

cd /d "%~dp0.."

echo ========================================
echo  Rag-AI - starting local stack
echo ========================================
echo.

call "%~dp0check-env.bat"
if errorlevel 1 (
  echo.
  echo Fix missing tools, then run start-all again.
  exit /b 1
)

echo.
echo [1/3] Starting Qdrant...
call "%~dp0start-qdrant.bat"
if errorlevel 1 (
  echo [ERROR] Qdrant failed to start.
  exit /b 1
)

echo.
echo [2/3] Opening API window...
start "Rag-AI API" cmd /k "%~dp0start-api.bat"

echo [3/3] Opening Web window...
start "Rag-AI Web" cmd /k "%~dp0start-web.bat"

echo.
echo ========================================
echo  Stack launch requested
echo ========================================
echo  Web:    http://localhost:3000
echo  API:    http://localhost:8000
echo  Health: http://localhost:8000/health
echo  Qdrant: http://localhost:6333
echo.
echo  Reminder: start Ollama locally if you use chat/embeddings later
echo            ollama serve   (or use the Ollama app)
echo            http://localhost:11434
echo ========================================
echo.
endlocal
