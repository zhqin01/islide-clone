@echo off
cd /d "%~dp0iSlideAddIn"
echo === Building iSlide Clone (.NET Framework 4.8) ===

set "CSC=C:\Windows\Microsoft.NET\Framework64\v4.0.30319\csc.exe"
set "REGASM=C:\Windows\Microsoft.NET\Framework64\v4.0.30319\regasm.exe"
set "GAC=C:\Windows\assembly\GAC_MSIL"
set "OUT=bin\Release\netfx\iSlideAddIn.dll"

mkdir bin\Release\netfx 2>nul

echo Compiling...

%CSC% /nologo /target:library /platform:x64 /out:"%OUT%" ^
  /r:"%GAC%\Microsoft.Office.Interop.PowerPoint\15.0.0.0__71e9bce111e9429c\Microsoft.Office.Interop.PowerPoint.dll" ^
  /r:"%GAC%\office\15.0.0.0__71e9bce111e9429c\office.dll" ^
  /r:System.Windows.Forms.dll /r:System.Drawing.dll ^
  AddInModule.cs RibbonManager.cs ^
  Features\FontManager.cs Features\ParagraphManager.cs Features\AlignmentManager.cs ^
  Features\SizeManager.cs Features\LayoutManager.cs Features\ColorManager.cs ^
  Features\PasteSwapManager.cs Features\WatermarkManager.cs Features\ProtectionManager.cs ^
  Features\SlideManager.cs Features\TweenManager.cs Features\ImageExportManager.cs ^
  Features\CompressManager.cs ^
  Dialogs\MatrixLayoutDialog.cs Dialogs\CircularLayoutDialog.cs ^
  Dialogs\WatermarkDialog.cs Dialogs\CompressDialog.cs ^
  Dialogs\ExportDialog.cs Dialogs\SlideSorterDialog.cs

if %ERRORLEVEL% NEQ 0 (
    echo BUILD FAILED — check errors above
    pause
    exit /b 1
)
echo Build OK

echo.
echo === Registering COM (admin required) ===
powershell -Command "Start-Process '%REGASM%' -ArgumentList '/codebase','%CD%\%OUT%' -Verb RunAs -Wait"
echo.

echo Adding PowerPoint AddIn keys...
reg add "HKCU\SOFTWARE\Microsoft\Office\PowerPoint\AddIns\iSlideAddIn.Connect" /v FriendlyName /t REG_SZ /d "iSlide Clone" /f
reg add "HKCU\SOFTWARE\Microsoft\Office\PowerPoint\AddIns\iSlideAddIn.Connect" /v Description /t REG_SZ /d "iSlide Clone - Offline Tools" /f
reg add "HKCU\SOFTWARE\Microsoft\Office\PowerPoint\AddIns\iSlideAddIn.Connect" /v LoadBehavior /t REG_DWORD /d 3 /f

echo.
echo === DONE ===
echo Close all PowerPoint windows and reopen.
pause
