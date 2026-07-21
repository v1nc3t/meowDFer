@echo off
:: Disable MSYS/Git-Bash path conversion so POSIX paths map cleanly
set MSYS_NO_PATHCONV=1

:: Check if the image exists, if not build it automatically from the script's directory (%~dp0)
docker image inspect meowdfer:latest >nul 2>&1
if %errorlevel% neq 0 (
    echo First time setup: Building Docker image...
    docker build -t meowdfer:latest "%~dp0"
)

:: Double quotes around "%cd%" ensure paths containing spaces map properly
docker run --rm -it -v "%cd%:%cd%" -w "%cd%" meowdfer:latest %*