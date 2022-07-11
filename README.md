## Prerequisites

Python 3, pip and venv

## Install and run

### Development

Generate and activate a venv :

```bash
python3 -m venv env 
. venv/bin/activate
```

Once in the venv, install dependencies :

```bash
pip install -r requirements.txt
```

Then start flask embeded server :

```bash
./commands/bash/start.sh
```

Server starts on port 5000. However, you need to prepare the database first during the first install :

```bash
./commands/bash/db-init.sh
./commands/bash/db-load-data.sh
./commands/bash/db-generate-trips.sh
```

Now you're ready to go ! Browse to `http://localhost:5000/trips/search/bordeaux` to test.

### Production deployement

Quick way to download, install and run with gunicorn, for the example (~3 minutes).

Make sure to have Python3, pip, venv available before running.

```bash
git clone git@github.com:ibcht/tchou-server.git
cd tchou-server
python3 -m venv venv
. venv/bin/activate
pip install wheel gunicorn
pip install .
export FLASK_APP=tchou
flask db:init # initialize database
flask db:load-data # load GTFS data 
flask db:generate-trips # trips calculation
gunicorn -w 4 'tchou:create_app()' # run webserver
```

Warning : this will create a sqlite3 database in the venv tchou instance by default, which is not recommended. See the Configuration section to customize this.

## Configure tchou-server

Run the app with the environment variable `TCHOU_SETTINGS=/path/to/config.py` (absolute path only), so you can override the default configuration.

Configuration available :

```python
DATABASE='/path/to/tchou.sqlite' #absolute path only
SECRET_KEY='dev'
ALLOW_ORIGIN='http://front-end-server.com' # Access-Control-Allow-Origin header value
# to be continued ...
```