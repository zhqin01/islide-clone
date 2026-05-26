# iSlide Clone - COM Registration
# Run as Administrator in Windows PowerShell.

$ErrorActionPreference = "Stop"
$dll = "C:\Users\Administrator\islide-clone\iSlideAddIn\bin\Release\net8.0-windows\iSlideAddIn.comhost.dll"
$guid = "F1A2B3C4-D5E6-7890-ABCD-EF0123456789"
$progId = "iSlideAddIn.Connect"

Write-Host "=== iSlide Clone COM Registration ===" -ForegroundColor Green
Write-Host "DLL: $dll"
Write-Host "GUID: {$guid}"
Write-Host ""

# Check DLL
if (-not (Test-Path $dll)) { Write-Host "ERROR: DLL not found!" -ForegroundColor Red; pause; exit 1 }

# Step 1: Let the .NET comhost register its own COM entries.
Write-Host "[1/2] Registering .NET COM host..."
$regsvr32 = Join-Path $env:WINDIR "System32\regsvr32.exe"
$p = Start-Process -FilePath $regsvr32 -ArgumentList "/s", "`"$dll`"" -Wait -PassThru -WindowStyle Hidden
if ($p.ExitCode -ne 0) {
    throw "regsvr32 failed with exit code $($p.ExitCode). Start PowerShell as Administrator and try again."
}
Write-Host "  COM host OK" -ForegroundColor Green

# Step 2: PowerPoint AddIn under HKCU
Write-Host "[2/2] Writing PowerPoint AddIn entry..."
$addinPath = "HKCU:\SOFTWARE\Microsoft\Office\PowerPoint\AddIns\$progId"
New-Item -Path $addinPath -Force | Out-Null
Set-ItemProperty -Path $addinPath -Name "FriendlyName" -Value "iSlide Clone" -Type String
Set-ItemProperty -Path $addinPath -Name "Description" -Value "iSlide Clone - Offline PowerPoint Tools" -Type String
Set-ItemProperty -Path $addinPath -Name "LoadBehavior" -Value 3 -Type DWord
Write-Host "  HKCU AddIn OK" -ForegroundColor Green

# Verify
Write-Host ""
Write-Host "=== Verification ==="
$clsidPath = "HKLM:\SOFTWARE\Classes\CLSID\{$guid}"
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
