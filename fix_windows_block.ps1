# Script om Windows Defender uitzondering toe te voegen voor Streamlit
# MOET ALS ADMINISTRATOR WORDEN GEDRAAID

Write-Host "========================================" -ForegroundColor Cyan
Write-Host "Windows Defender Uitzondering Toevoegen" -ForegroundColor Cyan
Write-Host "========================================" -ForegroundColor Cyan
Write-Host ""

# Check of script als admin draait
$isAdmin = ([Security.Principal.WindowsPrincipal] [Security.Principal.WindowsIdentity]::GetCurrent()).IsInRole([Security.Principal.WindowsBuiltInRole]::Administrator)

if (-not $isAdmin) {
    Write-Host "WAARSCHUWING: Dit script moet als Administrator worden gedraaid!" -ForegroundColor Red
    Write-Host ""
    Write-Host "Rechtsklik op PowerShell en kies 'Als Administrator uitvoeren'" -ForegroundColor Yellow
    Write-Host "Of voer dit commando uit:" -ForegroundColor Yellow
    Write-Host "  Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser" -ForegroundColor Green
    Write-Host ""
    pause
    exit 1
}

# Huidige directory
$projectPath = "C:\Users\TiborgWulffelevanMaa\OneDrive - Maatwerk Online\Documenten\geo-content-optimaliseren"

Write-Host "Toevoegen uitzondering voor project directory..." -ForegroundColor Yellow
Write-Host "Pad: $projectPath" -ForegroundColor Gray
Write-Host ""

try {
    # Voeg uitzondering toe
    Add-MpPreference -ExclusionPath $projectPath -ErrorAction Stop
    Write-Host "[OK] Uitzondering toegevoegd voor project directory" -ForegroundColor Green
    
    # Voeg ook Python toe (als die nog niet bestaat)
    $pythonPath = (Get-Command python).Source
    $pythonDir = Split-Path $pythonPath
    Add-MpPreference -ExclusionPath $pythonDir -ErrorAction SilentlyContinue
    Write-Host "[OK] Uitzondering toegevoegd voor Python directory" -ForegroundColor Green
    
    Write-Host ""
    Write-Host "========================================" -ForegroundColor Cyan
    Write-Host "SUCCES!" -ForegroundColor Green
    Write-Host "========================================" -ForegroundColor Cyan
    Write-Host ""
    Write-Host "Je kunt nu Streamlit proberen te starten:" -ForegroundColor Yellow
    Write-Host "  cd '$projectPath'" -ForegroundColor Green
    Write-Host "  streamlit run app.py" -ForegroundColor Green
    Write-Host ""
    
} catch {
    Write-Host "[FOUT] Kon uitzondering niet toevoegen: $($_.Exception.Message)" -ForegroundColor Red
    Write-Host ""
    Write-Host "Mogelijke oorzaken:" -ForegroundColor Yellow
    Write-Host "- Windows Defender is uitgeschakeld of beheerd door groepbeleid" -ForegroundColor Gray
    Write-Host "- Je hebt geen rechten om uitzonderingen toe te voegen" -ForegroundColor Gray
    Write-Host "- Neem contact op met ICT voor hulp" -ForegroundColor Gray
    Write-Host ""
}

pause
