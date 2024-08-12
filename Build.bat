@echo off
echo Cleaning up old builds...
rmdir /s /q build dist
del /f /q *.spec

echo Installing required packages...
pip install -r requirements.txt

echo Building the executable...
pyinstaller -D --uac-admin --onefile  ^
           --add-data "hidapi.dll;." ^
           --add-data "controllers;controllers" ^
           --add-data "emulators;emulators" ^
           --add-data "gui;gui" ^
           --icon="gui/img/favicon.png" ^
           --name="Gamepad King" main.py
echo Build complete!
pause