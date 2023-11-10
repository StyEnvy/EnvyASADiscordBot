@echo off
setlocal
set "BOT_DIR="

for /d /r "%~dp0" %%D in (EnvyGames) do (
    if exist "%%D\bot.py" (
        set "BOT_DIR=%%D"
        goto :found
    )
)
echo Could not find the EnvyGames directory with bot.py.
goto :eof

:found
cd /d "%BOT_DIR%"
echo Starting Discord Bot...
python bot.py
pause
endlocal
