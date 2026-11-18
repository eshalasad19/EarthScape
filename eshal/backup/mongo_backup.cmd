@echo off
rem mongo_backup.cmd (Eshal / Alizah) - MongoDB backup with mongodump.
rem Needs MongoDB Database Tools (mongodump). mongodump asks for the password in the window.
rem Usage:  mongo_backup.cmd es_admin
if "%1"=="" (echo Usage: mongo_backup.cmd ^<admin-user^> & exit /b 1)
for /f %%i in ('powershell -NoProfile -Command "Get-Date -Format yyyy-MM-dd"') do set D=%%i
if not exist C:\earthscape-backups\mongo mkdir C:\earthscape-backups\mongo
mongodump --db earthscape --username %1 --authenticationDatabase earthscape --out C:\earthscape-backups\mongo\backup-%D%
echo Backup saved in C:\earthscape-backups\mongo\backup-%D%