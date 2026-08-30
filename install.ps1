#Requires -Version 5.1
<#
.SYNOPSIS
  Build the meowDFer Docker image and register a User-PATH launcher.
#>
$ErrorActionPreference = "Stop"

$ProjectFolder = (Split-Path -Parent $MyInvocation.MyCommand.Path).TrimEnd('\')
Set-Location $ProjectFolder

Write-Host "Installing meowDFer for Windows..." -ForegroundColor Green

if (-not (Get-Command docker -ErrorAction SilentlyContinue)) {
    Write-Error "Docker Desktop is not installed or not available in PATH."
    exit 1
}

try {
    docker info 1>$null 2>$null
    if ($LASTEXITCODE -ne 0) { throw "docker info failed" }
} catch {
    Write-Error "Docker daemon is not running. Start Docker Desktop and retry."
    exit 1
}

Write-Host "Building Docker image..." -ForegroundColor Cyan
docker build -t meowdfer:latest $ProjectFolder
if ($LASTEXITCODE -ne 0) {
    Write-Error "Docker build failed."
    exit 1
}

Write-Host "Adding project folder to User PATH..." -ForegroundColor Cyan
$UserPath = [Environment]::GetEnvironmentVariable("Path", "User")
if ($null -eq $UserPath) { $UserPath = "" }

$NormalizedPaths = @()
if (-not [string]::IsNullOrWhiteSpace($UserPath)) {
    $NormalizedPaths = ($UserPath -split ';') | ForEach-Object { $_.TrimEnd('\') } | Where-Object { $_ }
}

if ($NormalizedPaths -contains $ProjectFolder) {
    Write-Host "Folder is already present in your PATH." -ForegroundColor Yellow
} else {
    if ([string]::IsNullOrWhiteSpace($UserPath)) {
        $NewPath = $ProjectFolder
    } elseif ($UserPath.EndsWith(";")) {
        $NewPath = "$UserPath$ProjectFolder"
    } else {
        $NewPath = "$UserPath;$ProjectFolder"
    }
    [Environment]::SetEnvironmentVariable("Path", $NewPath, "User")
    Write-Host "Folder added to User PATH." -ForegroundColor Green
}

Write-Host "Installation complete. Restart your terminal, then run 'meowdfer --help'." -ForegroundColor Green
