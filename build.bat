@echo off
cd /d "%~dp0"

echo ==========================================
echo   SlideKit — Build Script
echo ==========================================
echo.
echo [1] Build Python EXE (standalone .exe)
echo [2] Build C# COM Add-in (PowerPoint ribbon)
echo [3] Build Both
echo [4] Create Installer Package
echo.
set /p choice="Choose (1-4): "

if "%choice%"=="1" goto build_python
if "%choice%"=="2" goto build_csharp
if "%choice%"=="3" goto build_both
if "%choice%"=="4" goto build_installer
echo Invalid choice.
pause
exit /b 1

:build_python
echo.
echo === Building Python EXE with PyInstaller ===
pyinstaller build.spec --noconfirm
if %ERRORLEVEL% NEQ 0 (
    echo PYTHON BUILD FAILED
    pause
    exit /b 1
)
echo Python EXE built: dist\SlideKit.exe
goto :end

:build_csharp
echo.
echo === Building C# COM Add-in ===
cd /d "%~dp0SlideKit"

set "CSC=C:\Windows\Microsoft.NET\Framework64\v4.0.30319\csc.exe"
set "REGASM=C:\Windows\Microsoft.NET\Framework64\v4.0.30319\regasm.exe"
set "GAC=C:\Windows\assembly\GAC_MSIL"
set "OUT=bin\Release\netfx\SlideKit.dll"

mkdir bin\Release\netfx 2>nul

%CSC% /nologo /target:library /platform:x64 /out:"%OUT%" ^
  /r:"%GAC%\Microsoft.Office.Interop.PowerPoint\15.0.0.0__71e9bce111e9429c\Microsoft.Office.Interop.PowerPoint.dll" ^
  /r:"%GAC%\office\15.0.0.0__71e9bce111e9429c\office.dll" ^
  /r:System.Windows.Forms.dll /r:System.Drawing.dll ^
  SlideKit.csproj AddInModule.cs RibbonManager.cs ^
  Features\FontManager.cs Features\ParagraphManager.cs Features\AlignmentManager.cs ^
  Features\SizeManager.cs Features\LayoutManager.cs Features\ColorManager.cs ^
  Features\PasteSwapManager.cs Features\WatermarkManager.cs Features\ProtectionManager.cs ^
  Features\SlideManager.cs Features\TweenManager.cs Features\ImageExportManager.cs ^
  Features\CompressManager.cs ^
  Dialogs\MatrixLayoutDialog.cs Dialogs\CircularLayoutDialog.cs ^
  Dialogs\WatermarkDialog.cs Dialogs\CompressDialog.cs ^
  Dialogs\ExportDialog.cs Dialogs\SlideSorterDialog.cs

if %ERRORLEVEL% NEQ 0 (
    echo C# BUILD FAILED
    pause
    exit /b 1
)
echo C# build OK: %OUT%
cd /d "%~dp0"
goto :end

:build_both
call :build_python
call :build_csharp
goto :end

:build_installer
echo.
echo === Creating Installer Package ===
if not exist "dist\SlideKit.exe" (
    echo SlideKit.exe not found. Run Python build first.
    pause
    exit /b 1
)
rmdir /s /q "installer\SlideKit" 2>nul
mkdir "installer\SlideKit"
copy "dist\SlideKit.exe" "installer\SlideKit\"
copy "installer\install.ps1" "installer\SlideKit\"
copy "installer\setup.bat" "installer\SlideKit\"
echo Installer created: installer\SlideKit\
echo.
echo Run installer\SlideKit\setup.bat to install.
goto :end

:end
echo.
echo === DONE ===
pause
