@echo off
setlocal ENABLEEXTENSIONS
echo Get macOS VMware Tools 3.0.5
echo ===============================
echo (c) Dave Parsons 2011-21

net session >NUL 2>&1
if %errorlevel% neq 0 (
    echo Administrator privileges required!
    exit
)

pushd %~dp0
.\python-win-embed-amd64\python.exe gettools.py
popd
