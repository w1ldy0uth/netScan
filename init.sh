#!/bin/bash

VENV_NAME="netscan_venv"

python -m venv "$VENV_NAME"
source "$VENV_NAME/bin/activate"

pip install -r requirements.txt

echo "Virtual environment '$VENV_NAME' is set up and activated."
echo "Packages from requirements.txt are installed."
