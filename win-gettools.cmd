@echo off
setlocal ENABLEEXTENSIONS
echo Get macOS VMware Tools 3.0.5
echo ===============================
echo (c) Dave Parsons 2011-21

pushd %~dp0
.\python-win-embed-amd64\python.exe gettools.py
popd
