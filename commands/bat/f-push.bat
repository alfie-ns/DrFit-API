@echo off

REM Force push to main branch and clear all previous commits

cd .. cd ..
git add .
git commit -m "Clear all previous commits"
git push origin main --force
