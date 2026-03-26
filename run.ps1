Set-StrictMode -Version Latest
$ErrorActionPreference = "Stop"

Set-Location $PSScriptRoot

if (-not (Test-Path ".\\venv\\Scripts\\Activate.ps1")) {
  python -m venv venv
}

. .\\venv\\Scripts\\Activate.ps1
pip install -r requirements.txt

python .\\backend\\app.py

