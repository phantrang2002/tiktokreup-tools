#run_main.ps1
#Kích hoạt venv
$venvPath = ".\venv\Scripts\Activate.ps1"
if (Test-Path $venvPath) {
    Write-Host "Activating virtual environment..."
    & $venvPath
} else {
    Write-Host "❌ Virtual environment not found at $venvPath"
    exit
}

#Chạy main.py
Write-Host "Running main.py..."
python .\main.py

#Tắt venv
Write-Host "Deactivating virtual environment..."
deactivate

Write-Host "✅ Done!"
