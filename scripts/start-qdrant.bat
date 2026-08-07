@echo off
setlocal
title Rag-AI Qdrant

cd /d "%~dp0.."

call "%~dp0ensure-docker.bat"
if errorlevel 1 (
  exit /b 1
)

echo Starting Qdrant...
docker compose -f docker\docker-compose.yml up -d
if errorlevel 1 (
  echo [WARN] Compose failed to start rag-ai-qdrant.
  echo        Checking if something is already serving Qdrant on :6333...
  powershell -NoProfile -Command "try { $r = Invoke-WebRequest -Uri 'http://localhost:6333/readyz' -UseBasicParsing -TimeoutSec 3; if ($r.StatusCode -ge 200 -and $r.StatusCode -lt 500) { exit 0 } else { exit 1 } } catch { try { $r = Invoke-WebRequest -Uri 'http://localhost:6333/' -UseBasicParsing -TimeoutSec 3; exit 0 } catch { exit 1 } }"
  if errorlevel 1 (
    echo [ERROR] Failed to start Qdrant and nothing is listening on :6333.
    exit /b 1
  )
  echo [OK] Qdrant already available at http://localhost:6333
  echo      ^(another container may be using the port — that is fine for Rag-AI^)
  endlocal
  exit /b 0
)

echo Qdrant is up at http://localhost:6333
endlocal
