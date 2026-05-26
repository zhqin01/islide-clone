# iSlide Clone - Manual COM Registration
# Run as Administrator in PowerShell

$ErrorActionPreference = "Continue"
$dll = "C:\Users\Administrator\islide-clone\iSlideAddIn\bin\Release\net8.0-windows\iSlideAddIn.comhost.dll"
$guid = "F1A2B3C4-D5E6-7890-ABCD-EF0123456789"
$progId = "iSlideAddIn.Connect"

Write-Host "=== iSlide Clone COM Registration ===" -ForegroundColor Green
Write-Host "DLL: $dll"
Write-Host "GUID: {$guid}"
Write-Host ""

# Check DLL
if (-not (Test-Path $dll)) { Write-Host "ERROR: DLL not found!" -ForegroundColor Red; pause; exit 1 }

# Step 1: Register CLSID under HKLM (requires Admin)
Write-Host "[1/3] Writing HKLM CLSID entries..."
$clsidPath = "HKLM:\SOFTWARE\Classes\CLSID\{$guid}"
New-Item -Path $clsidPath -Force | Out-Null
Set-ItemProperty -Path $clsidPath -Name "(Default)" -Value $progId -Type String

$inprocPath = "$clsidPath\InprocServer32"
New-Item -Path $inprocPath -Force | Out-Null
Set-ItemProperty -Path $inprocPath -Name "(Default)" -Value $dll -Type String
Set-ItemProperty -Path $inprocPath -Name "ThreadingModel" -Value "Both" -Type String

$progIdPath = "$clsidPath\ProgId"
New-Item -Path $progIdPath -Force | Out-Null
Set-ItemProperty -Path $progIdPath -Name "(Default)" -Value $progId -Type String
Write-Host "  HKLM CLSID OK" -ForegroundColor Green

# Step 2: ProgId under HKLM
Write-Host "[2/3] Writing HKLM ProgId entries..."
$progIdRegPath = "HKLM:\SOFTWARE\Classes\$progId"
New-Item -Path $progIdRegPath -Force | Out-Null
Set-ItemProperty -Path $progIdRegPath -Name "(Default)" -Value "iSlide Clone AddIn" -Type String
$progIdClsidPath = "$progIdRegPath\CLSID"
New-Item -Path $progIdClsidPath -Force | Out-Null
Set-ItemProperty -Path $progIdClsidPath -Name "(Default)" -Value "{$guid}" -Type String
Write-Host "  HKLM ProgId OK" -ForegroundColor Green

# Step 3: PowerPoint AddIn under HKCU
Write-Host "[3/3] Writing HKCU PowerPoint AddIn entry..."
$addinPath = "HKCU:\SOFTWARE\Microsoft\Office\PowerPoint\AddIns\$progId"
New-Item -Path $addinPath -Force | Out-Null
Set-ItemProperty -Path $addinPath -Name "FriendlyName" -Value "iSlide Clone" -Type String
Set-ItemProperty -Path $addinPath -Name "Description" -Value "iSlide Clone - Offline PowerPoint Tools" -Type String
Set-ItemProperty -Path $addinPath -Name "LoadBehavior" -Value 3 -Type DWord
Write-Host "  HKCU AddIn OK" -ForegroundColor Green

# Verify
Write-Host ""
Write-Host "=== Verification ==="
if (Test-Path $clsidPath) {
    Write-Host "PASS: CLSID registered in HKLM" -ForegroundColor Green
} else {
    Write-Host "FAIL: CLSID not in HKLM" -ForegroundColor Red
}
if (Test-Path $addinPath) {
    $lb = Get-ItemProperty -Path $addinPath
    Write-Host "PASS: AddIn entry found (LoadBehavior=$($lb.LoadBehavior))" -ForegroundColor Green
} else {
    Write-Host "FAIL: AddIn entry not found" -ForegroundColor Red
}

Write-Host ""
Write-Host "DONE! Close all PowerPoint windows and reopen." -ForegroundColor Green
Write-Host "Check ribbon for 'iSlide' tab."
pause
