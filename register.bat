@echo off
cd /d "%~dp0"
echo Requesting administrator privileges...
powershell -Command "Start-Process powershell -ArgumentList '-ExecutionPolicy Bypass -File \"%~dp0register.ps1\"' -Verb RunAs"
pause
