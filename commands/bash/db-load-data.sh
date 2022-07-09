source "${0%/*}/env"
export FLASK_APP
export FLASK_ENV

read -p "You are loading new data. Are you sure ? (y/n)" confirm

if [[ "$confirm" =~ [yY] ]]; then
    flask db:load-data
    echo "Command complete."
else
    echo "Cancel ..."
fi
