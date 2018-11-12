@echo off

call venv\Scripts\activate
pyInstaller --onefile mouseGesture.py

pause