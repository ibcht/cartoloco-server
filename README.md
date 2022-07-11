## Prerequisites

Python 3, pip and venv

## Startup

### Development stage

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

## Configure tchou-server

### Development usage

Copy the ./instance/config.sample.py file to ./instance/config.py to override default settings.

### Production usage

Run the app with the environment variable `TCHOU_SETTINGS=/path/to/config.py`, so the external configuration is possible.