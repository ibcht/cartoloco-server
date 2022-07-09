source "${0%/*}/env"
export FLASK_APP
export FLASK_ENV

read -p "!!! You are purging db and reseting the schema. Are you sure ? (y/n) : " confirm
if [[ "$confirm" =~ [yY] ]]; then
    flask db:init
    echo "Command complete."
else
    echo "Cancel ..."
fi

