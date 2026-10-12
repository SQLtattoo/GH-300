# Budget Buddy Demo Setup Script

param(
    [switch]$SkipTests,
    [switch]$Force
)

$ErrorActionPreference = "Stop"

function Write-Step($Message) {
    Write-Host "`n==> $Message" -ForegroundColor Cyan
}

function Write-Ok($Message) {
    Write-Host "  OK  $Message" -ForegroundColor Green
}

function Write-Info($Message) {
    Write-Host "  ..  $Message" -ForegroundColor Gray
}

Write-Step "Checking Python"
$pythonVersion = python --version
Write-Ok $pythonVersion

Write-Step "Preparing virtual environment"
if ((Test-Path ".venv") -and $Force) {
    Remove-Item -Recurse -Force ".venv"
}

if (-not (Test-Path ".venv")) {
    python -m venv .venv
    Write-Ok "Created .venv"
} else {
    Write-Ok "Using existing .venv"
}

Write-Step "Installing test dependencies"
.\.venv\Scripts\python.exe -m pip install --upgrade pip --quiet
.\.venv\Scripts\python.exe -m pip install -r requirements-test.txt --quiet
Write-Ok "Dependencies installed"

Write-Step "Running Budget Buddy app"
.\.venv\Scripts\python.exe main.py
Write-Ok "App runs"

if (-not $SkipTests) {
    Write-Step "Running test suite"
    .\.venv\Scripts\python.exe -m pytest
    Write-Ok "Tests passed"
}

Write-Step "Next demo commands"
Write-Info ".\.venv\Scripts\Activate.ps1"
Write-Info "python main.py"
Write-Info "pytest"
Write-Info "Open DEMO_SCRIPT.md for the trainer flow"