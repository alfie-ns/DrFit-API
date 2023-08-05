@echo off

REM Reattach to main branch if getting selected repository

cd .. cd ..
git branch my-temporary-work
git checkout main  
git merge my-temporary-work