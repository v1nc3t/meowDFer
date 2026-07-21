# Get the absolute folder path where this installation script is located (trimmed of trailing slashes)
$ProjectFolder = (Split-Path -Parent $MyInvocation.MyCommand.Path).TrimEnd('\')

Write-Host "Installing meowDFer for Windows..." -ForegroundColor Green

# 1. Verify Docker CLI is accessible
if (-not (Get-Command docker -ErrorAction SilentlyContinue)) {
    Write-Error "Docker Desktop is not installed or not running in your environment PATH."
    Exit 1
}

# 2. Build the Docker container image
Write-Host "Building Docker container..." -ForegroundColor Cyan
docker build -t meowdfer:latest "$ProjectFolder"

# 3. Permanently add the project directory to the User's PATH environment variable
Write-Host "Adding folder to User Environment Path..." -ForegroundColor Cyan
$UserPath = [Environment]::GetEnvironmentVariable("Path", "User")

# Split existing path and normalize entries to remove trailing slashes for comparison
$NormalizedPaths = ($UserPath -split ';') | ForEach-Object { $_.TrimEnd('\') }

if ($NormalizedPaths -contains $ProjectFolder) {
    Write-Host "Folder is already present in your PATH." -ForegroundColor Yellow
} else {
    # Safely append to PATH without creating double semicolons
    if ([string]::IsNullOrWhiteSpace($UserPath)) {
        $NewPath = $ProjectFolder
    } elseif ($UserPath.EndsWith(";")) {
        $NewPath = "$UserPath$ProjectFolder"
    } else {
        $NewPath = "$UserPath;$ProjectFolder"
    }

    [Environment]::SetEnvironmentVariable("Path", $NewPath, "User")
    Write-Host "Folder permanently added to your User PATH environment variable." -ForegroundColor Green
}

Write-Host "Installation complete! Please RESTART your Terminal / Command Prompt to refresh the PATH context." -ForegroundColor Green