# ==============================================================================
# PauliBot Local Development Setup Script
# ==============================================================================
# Run this script to set up your local development environment
# Usage: .\setup_local.ps1
# ==============================================================================

Write-Host "===========================================" -ForegroundColor Cyan
Write-Host "  PauliBot Local Development Setup" -ForegroundColor Cyan
Write-Host "===========================================" -ForegroundColor Cyan
Write-Host ""

# Step 1: Activate virtual environment
Write-Host "[1/5] Activating virtual environment..." -ForegroundColor Yellow
& ".\venv\Scripts\Activate.ps1"

# Step 2: Install dependencies
Write-Host "[2/5] Installing Python dependencies..." -ForegroundColor Yellow
python -m pip install --upgrade pip
pip install -r requirements.txt

# Step 3: Create migrations
Write-Host "[3/5] Creating database migrations..." -ForegroundColor Yellow
python manage.py makemigrations

# Step 4: Apply migrations
Write-Host "[4/5] Applying database migrations..." -ForegroundColor Yellow
python manage.py migrate

# Step 5: Create superuser (optional)
Write-Host "[5/5] You can now create a superuser account (skip if testing guest mode)..." -ForegroundColor Yellow
$createSuperuser = Read-Host "Create superuser now? (y/n)"
if ($createSuperuser -eq "y") {
    python manage.py createsuperuser
}

Write-Host ""
Write-Host "===========================================" -ForegroundColor Green
Write-Host "  Setup Complete!" -ForegroundColor Green
Write-Host "===========================================" -ForegroundColor Green
Write-Host ""
Write-Host "To start the development server, run:" -ForegroundColor Cyan
Write-Host "  python manage.py runserver" -ForegroundColor White
Write-Host ""
Write-Host "Then open your browser to:" -ForegroundColor Cyan
Write-Host "  http://localhost:8000" -ForegroundColor White
Write-Host ""
