@echo off

set VENV_NAME=netscan_venv

python -m venv %VENV_NAME%
call %VENV_NAME%\Scripts\activate

pip install -r requirements.txt

echo Virtual environment '%VENV_NAME%' is set up and activated.
echo Packages from requirements.txt are installed.
