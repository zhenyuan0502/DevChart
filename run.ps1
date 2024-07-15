# Activate environment
. .env/Scripts/Activate.ps1
# Run flask app
$env:FLASK_APP = "app.py"
$env:FLASK_ENV = "development"
$env:FLASK_DEBUG = 1
flask run