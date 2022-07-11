source "${0%/*}/env"
export FLASK_APP
export FLASK_ENV

read -p "!You are updating the 'trips' table. Are you sure ? (y/n)" confirm
if [[ "$confirm" =~ [yY] ]]; then
    flask db:generate-trips
    echo "Command complete."
else
    echo "Cancel ..."
fi

