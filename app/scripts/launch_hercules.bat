@echo off

rem Récupération du chemin courant
set current_path=D:/ADCD/
cd %current_path%

echo %current_path%
rem Lancer hercules
call start cmd /k "%current_path%hercules.exe -f %current_path%hercules.cnf"
