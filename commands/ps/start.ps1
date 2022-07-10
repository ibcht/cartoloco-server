#$ScriptDir = Split-Path $script:MyInvocation.MyCommand.Path
$ScriptDir = 'P:\dev\python-dev\tchou-server\tchou'
$env:FLASK_APP=$ScriptDir
$env:FLASK_ENV="development"
$env:TCHOU_SETTINGS='P:\dev\python-dev\tchou-server\instance\config.py'
flask run