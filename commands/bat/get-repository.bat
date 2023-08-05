@echo off

REM Get selected repository

cd .. cd ..
set repo_url=https://github.com/alfie-ns/drfit-Django-api
set commit_hash=be5db2f13fce4e35d90235b9ba1e14856625b3ae
set target_directory=new-dr-fit
git clone %repo_url% %target_directory%
cd %target_directory%
git fetch origin %commit_hash%
git checkout %commit_hash%
