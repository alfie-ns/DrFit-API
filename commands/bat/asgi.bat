@echo off

REM Run the Django server

cd..
daphne main.asgi:application