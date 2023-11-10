@echo off
setlocal

cd /d "%~dp0"

echo Checking virtual environment...
if not exist "venv\Scripts\activate.bat" (
    echo Creating virtual environment...
    python -m venv venv
)

echo Activating virtual environment...
call venv\Scripts\activate.bat

echo Installing dependencies...
pip install -r requirements.txt

cd EnvyGames
echo Starting Discord Bot...
python bot.py
pause
endlocal
