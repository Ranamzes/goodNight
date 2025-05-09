@echo off
set TASKNAME=Power Control API

REM Check if the task already exists
schtasks /query /tn "%TASKNAME%" >nul 2>&1
if %errorlevel%==0 (
    echo Task already exists. Deleting the old version...
    schtasks /delete /tn "%TASKNAME%" /f
)

REM Create the new task
schtasks /create /xml "%~dp0power_control_task.xml" /tn "%TASKNAME%"
if %errorlevel%==0 (
    echo Service installed successfully!
) else (
    echo ERROR during service installation!
    pause
    exit /b 1
)

REM (Optional) Run the task manually for testing
REM schtasks /run /tn "%TASKNAME%"

pause
