@echo off
setlocal EnableDelayedExpansion

where docker >nul 2>&1
if errorlevel 1 (
  echo [ERROR] Docker is not on PATH. Install Docker Desktop and try again.
  exit /b 1
)

docker info >nul 2>&1
if not errorlevel 1 (
  echo [OK] Docker engine is already running.
  exit /b 0
)

echo Docker engine is not running. Launching Docker Desktop...

set "DOCKER_DESKTOP="
if exist "%ProgramFiles%\Docker\Docker\Docker Desktop.exe" (
  set "DOCKER_DESKTOP=%ProgramFiles%\Docker\Docker\Docker Desktop.exe"
) else if exist "%LocalAppData%\Docker\Docker Desktop.exe" (
  set "DOCKER_DESKTOP=%LocalAppData%\Docker\Docker Desktop.exe"
) else if exist "%ProgramFiles%\Docker\Docker\DockerDesktop.exe" (
  set "DOCKER_DESKTOP=%ProgramFiles%\Docker\Docker\DockerDesktop.exe"
)

if not defined DOCKER_DESKTOP (
  echo [ERROR] Could not find Docker Desktop.exe
  echo         Start Docker Desktop manually, then retry.
  exit /b 1
)

start "" "!DOCKER_DESKTOP!"

set /a ATTEMPTS=0
:wait_loop
set /a ATTEMPTS+=1
docker info >nul 2>&1
if not errorlevel 1 (
  echo [OK] Docker engine is ready.
  exit /b 0
)

if !ATTEMPTS! GEQ 40 (
  echo [ERROR] Timed out waiting for Docker Desktop ^(about 2 minutes^).
  echo         Open Docker Desktop and wait until it says it is running, then retry.
  exit /b 1
)

echo Waiting for Docker Desktop... (!ATTEMPTS!/40)
timeout /t 3 /nobreak >nul
goto wait_loop
