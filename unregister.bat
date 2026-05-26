@echo off
cd /d "%~dp0"
echo Requesting administrator privileges to unregister...
powershell -Command "Start-Process powershell -ArgumentList '-ExecutionPolicy Bypass -Command \"Remove-Item HKLM:\SOFTWARE\Classes\CLSID:\{F1A2B3C4-D5E6-7890-ABCD-EF0123456789\} -Recurse -Force -ErrorAction SilentlyContinue; Remove-Item HKLM:\SOFTWARE\Classes\iSlideAddIn.Connect -Recurse -Force -ErrorAction SilentlyContinue; Remove-Item HKCU:\SOFTWARE\Microsoft\Office\PowerPoint\AddIns\iSlideAddIn.Connect -Recurse -Force -ErrorAction SilentlyContinue; Write-Host Unregistered successfully.; pause\"' -Verb RunAs"
