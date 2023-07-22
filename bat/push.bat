@echo off

REM Push code to repository, pulling the latest changes first

cd ..
git pull origin main
git add -A
git commit -m "Update"
git push origin main