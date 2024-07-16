# Create python environment and store in .env
python -m venv .env
# Activate the environment
. .env/Scripts/Activate.ps1
python -m pip install --upgrade pip
# Install required packages
pip install -r requirements.txt


