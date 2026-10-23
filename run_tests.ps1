param(
    [ValidateSet("chrome", "edge")][string]$Browser = "chrome",
    [switch]$Headless
)

$ErrorActionPreference = "Stop"
Set-Location $PSScriptRoot
$python = Get-Command python -ErrorAction SilentlyContinue
if (-not $python) { throw "Python 3 is not available on PATH." }
if (-not (Test-Path ".venv\Scripts\python.exe")) {
    python -m venv .venv
}
& .\.venv\Scripts\python.exe -m pip install -r requirements.txt

$selectedSite = if ($env:SHOPSPHERE_SITE) { $env:SHOPSPHERE_SITE } else { "automation_exercise" }

$env:SHOPSPHERE_BROWSER = $Browser
$env:SHOPSPHERE_SITE = $selectedSite
if ($Headless) { $env:SHOPSPHERE_HEADLESS = "true" }

& .\.venv\Scripts\python.exe -m pytest tests/test_*.py -v --html=reports\report.html --self-contained-html
if ($LASTEXITCODE -ne 0) { exit $LASTEXITCODE }
