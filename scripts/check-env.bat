@echo off
setlocal EnableDelayedExpansion
title Rag-AI Check Env

set "FAILED=0"

echo Checking required tools...
echo.

where docker >nul 2>&1
if errorlevel 1 (
  echo [MISS] docker
  set "FAILED=1"
) else (
  echo [OK]   docker
)

where node >nul 2>&1
if errorlevel 1 (
  echo [MISS] node
  set "FAILED=1"
) else (
  for /f "tokens=*" %%v in ('node -v') do echo [OK]   node %%v
)

where npm >nul 2>&1
if errorlevel 1 (
  echo [MISS] npm
  set "FAILED=1"
) else (
  for /f "tokens=*" %%v in ('npm -v') do echo [OK]   npm %%v
)

where python >nul 2>&1
if errorlevel 1 (
  echo [MISS] python
  set "FAILED=1"
) else (
  for /f "tokens=*" %%v in ('python --version') do echo [OK]   %%v
)

where ollama >nul 2>&1
if errorlevel 1 (
  echo [WARN] ollama not on PATH ^(install later for RAG^)
) else (
  echo [OK]   ollama
)

echo.
if "!FAILED!"=="1" (
  echo Environment check failed. Install missing tools and retry.
  exit /b 1
)

echo Environment check passed.
exit /b 0
