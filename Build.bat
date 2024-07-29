@echo off
echo Cleaning up old builds...
rmdir /s /q build dist
del /f /q *.spec

echo Installing required packages...
pip install -r requirements.txt

echo Building the executable...
pyinstaller --noconfirm --onedir --windowed --add-data "config.yml;." --add-data "hidapi.dll;." --add-data "gui/img;gui/img" --icon="gui/img/favicon.png" --name="Gamepad King" main.py

echo Build complete!
pause