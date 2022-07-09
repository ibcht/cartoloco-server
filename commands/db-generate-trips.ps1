#$ScriptDir = Split-Path $script:MyInvocation.MyCommand.Path
$ScriptDir = 'P:\dev\python-dev\flask-tutorial\tchou\app'
$env:FLASK_APP=$ScriptDir
$env:FLASK_ENV="development"
$confirm=Read-Host -Prompt "You are updating the 'trips' table. Are you sure ? (y/n)"
if($confirm -eq 'y') {
    flask db:generate-trips
    Write-Host "Command complete."
} else {
    Write-Host "Cancel ..."
}
Start-Sleep -Seconds 1