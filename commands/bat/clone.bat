@echo off

REM Clone the repository to new-dr-fit 

cd .. cd ..
set repo_url=https://github.com/alfie-ns/drfit-Django-api
set target_directory=dr-fit-NEW
git clone %repo_url% %target_directory%
cd %target_directory%
