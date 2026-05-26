# iSlide Clone - Build & Register COM Add-in
# Run as Administrator for registration part

$ErrorActionPreference = "Stop"
$csc = "C:\Windows\Microsoft.NET\Framework64\v4.0.30319\csc.exe"
$regasm = "C:\Windows\Microsoft.NET\Framework64\v4.0.30319\regasm.exe"
$gac = "C:\Windows\assembly\GAC_MSIL"
$projDir = "C:\Users\Administrator\islide-clone\iSlideAddIn"
$outDir = "$projDir\bin\Release\netfx"
$outDll = "$outDir\iSlideAddIn.dll"

New-Item -ItemType Directory -Force -Path $outDir | Out-Null

$refs = @(
    "/r:$gac\Microsoft.Office.Interop.PowerPoint\15.0.0.0__71e9bce111e9429c\Microsoft.Office.Interop.PowerPoint.dll",
    "/r:$gac\office\15.0.0.0__71e9bce111e9429c\office.dll",
    "/r:System.Windows.Forms.dll",
    "/r:System.Drawing.dll"
)

$srcFeatures = Get-ChildItem "$projDir\Features\*.cs" | ForEach-Object { $_.FullName }
$srcDialogs = Get-ChildItem "$projDir\Dialogs\*.cs" | ForEach-Object { $_.FullName }
$srcMain = @("$projDir\AddInModule.cs", "$projDir\RibbonManager.cs")

$allSrc = $srcMain + $srcFeatures + $srcDialogs

Write-Host "=== Building iSlide Clone (.NET Framework 4.8) ===" -ForegroundColor Green
Write-Host "Compiler: $csc"
Write-Host "Output: $outDll"
Write-Host ""

$args = @("/nologo", "/target:library", "/platform:x64", "/out:$outDll") + $refs + $allSrc
Write-Host "Running csc.exe..."
& $csc $args 2>&1

if ($LASTEXITCODE -ne 0) {
    Write-Host "`nBUILD FAILED" -ForegroundColor Red
    Read-Host "Press Enter"
    exit 1
}

Write-Host "Build OK" -ForegroundColor Green
Write-Host ""

# Register COM
Write-Host "=== Registering COM (admin required) ===" -ForegroundColor Yellow
$regArgs = "/codebase", "`"$outDll`""
$proc = Start-Process $regasm -ArgumentList $regArgs -Verb RunAs -Wait -PassThru

if ($proc.ExitCode -ne 0) {
    Write-Host "regasm returned exit code: $($proc.ExitCode)" -ForegroundColor Yellow
}

# Add PowerPoint AddIn keys
Write-Host "Adding PowerPoint AddIn registry keys..."
$addinKey = "HKCU:\SOFTWARE\Microsoft\Office\PowerPoint\AddIns\iSlideAddIn.Connect"
New-Item -Path $addinKey -Force | Out-Null
Set-ItemProperty -Path $addinKey -Name "FriendlyName" -Value "iSlide Clone" -Type String
Set-ItemProperty -Path $addinKey -Name "Description" -Value "iSlide Clone - Offline Tools" -Type String
Set-ItemProperty -Path $addinKey -Name "LoadBehavior" -Value 3 -Type DWord

Write-Host ""
Write-Host "=== DONE ===" -ForegroundColor Green
Write-Host "Close all PowerPoint windows and reopen."
Write-Host "You should see the 'iSlide' tab in the ribbon."
Read-Host "Press Enter"
