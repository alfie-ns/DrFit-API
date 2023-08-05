@echo off

REM Delete all images in images directory

cd .. cd ..
set "directory=static\images"
del /q "%directory%\*"
