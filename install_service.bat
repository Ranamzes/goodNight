@echo off
schtasks /create /xml "%~dp0power_control_task.xml" /tn "Power Control API"
echo Служба установлена успешно
pause 
