@echo off
setlocal EnableExtensions

:: Disable MSYS/Git-Bash path conversion so Windows paths map cleanly into Docker.
set MSYS_NO_PATHCONV=1

where docker >nul 2>&1
if errorlevel 1 (
    echo Error: Docker is not installed or not in PATH.
    exit /b 1
)

docker info >nul 2>&1
if errorlevel 1 (
    echo Error: Docker daemon is not running. Start Docker Desktop and retry.
    exit /b 1
)

docker image inspect meowdfer:latest >nul 2>&1
if errorlevel 1 (
    echo First-time setup: building Docker image...
    docker build -t meowdfer:latest "%~dp0."
    if errorlevel 1 exit /b 1
)

:: Mount the user profile and current directory so absolute and relative paths resolve.
docker run --rm -it ^
    -e HOME=/tmp ^
    -v "%USERPROFILE%:%USERPROFILE%" ^
    -v "%CD%:%CD%" ^
    -w "%CD%" ^
    meowdfer:latest %*
exit /b %ERRORLEVEL%
