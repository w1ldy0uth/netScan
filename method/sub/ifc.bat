@echo off

FOR /F "tokens=3,*" %%A IN ('netsh interface show interface^|find "Connected"') DO echo %%B