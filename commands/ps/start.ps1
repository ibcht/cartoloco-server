#$ScriptDir = Split-Path $script:MyInvocation.MyCommand.Path
$ScriptDir = 'P:\dev\python-dev\flask-tutorial\tchou\tchou'
$env:FLASK_APP=$ScriptDir
$env:FLASK_ENV="development"
flask run