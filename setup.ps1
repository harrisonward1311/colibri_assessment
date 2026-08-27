# setup.ps1 - One-time environment setup for the Colibri pipeline

Write-Host "Creating virtual environment..." -ForegroundColor Cyan
py -m venv venv; & .\venv\Scripts\Activate.ps1

Write-Host "Installing dependencies..." -ForegroundColor Cyan
pip install -r requirements.txt

Write-Host "Setup complete" -ForegroundColor Green
