@echo off

REM Delete selected directory

set target_directory=dr-fit-NEW
cd ..
rmdir /s /q %target_directory%
