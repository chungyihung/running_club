@echo off
if "%PYTHON3%"=="" (
    SET PYTHON3=C:\Users\HungJoseph\AppData\Local\Programs\Python\Python36\python.exe
    ECHO PYTHON3 is not set, using default install path
) ELSE (
    ECHO PYTHON3 is set as [ %PYTHON% ]
)

%PYTHON3% main.py

