# AgroAI Quick Launcher
Write-Host "==========================================" -ForegroundColor Green
Write-Host "   Starting AgroAI Platform" -ForegroundColor Green
Write-Host "   Model 1: EfficientNet-B0 (38 Classes)" -ForegroundColor Yellow
Write-Host "   Bento Grid UI • Strictly No GenAI" -ForegroundColor Cyan
Write-Host "==========================================" -ForegroundColor Green

# 1. Start FastAPI Backend in background
Write-Host "`n[1/2] Starting FastAPI Backend on http://127.0.0.1:8000..." -ForegroundColor Green
$backendProcess = Start-Process -FilePath ".venv\Scripts\python.exe" -ArgumentList "backend\run.py" -PassThru -NoNewWindow

Start-Sleep -Seconds 3

# 2. Start Next.js Frontend
Write-Host "`n[2/2] Starting Next.js Frontend on http://localhost:3000..." -ForegroundColor Green
Set-Location frontend
npm run dev

