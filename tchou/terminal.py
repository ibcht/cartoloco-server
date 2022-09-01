#!python3

import time
import sqlite3
import core

# Disable interpolation to avoid parsing % as a special character
#conf = configparser.ConfigParser(interpolation=None)

#conf.read('api.ini','utf8')
#api_key = conf['sncf']['api_key']
#api_secret = conf['sncf']['api_secret']
# requests.get()

"""Terminal client"""

g = {}

database = ':memory:'

def get_db():
    if 'db' not in g:
        g['db'] = sqlite3.connect(database)
        g['db'].row_factory = sqlite3.Row
    return g['db']

def get_stop_index(clear = False):
    # choose 'clear' to delete existing values
    if 'stop_index' not in g or clear:
        g['stop_index'] = {}
    return g['stop_index']

# 2. Process trip claculation (must be done after step 1, everyday)
def process_trips():
    db = get_db()
    tripService = core.TripService(db)
    tripService.generate_trips()

# 3. Search for trips
def get_trips_from(source_index = 0):
    stop_index = get_stop_index()
    try:
        source = stop_index[int(source_index)]
        db = get_db()
        res = db.execute('select type, src_name, tgt_name, min_time, max_time from times where src_id = ? order by tgt_name asc',(source,)).fetchall()
        print('De                   | Vers                 | Durée         | Type')
        print('---------------------|----------------------|---------------|------------------')
        for r in res:
            # print(f'{r["src_name"].ljust(20)} | {r["tgt_name"].ljust(20)} | {str(r["min_time"]).rjust(3)} - {str(r["max_time"]).rjust(3)} min | {re.findall("OCE[^-]*",r["type"])[0]}')
            print(f'{r["src_name"].ljust(20)} | {r["tgt_name"].ljust(20)} | {str(r["min_time"]).rjust(3)} - {str(r["max_time"]).rjust(3)} min | {r["type"]}')
    except(KeyError):
        print('Cette gare n\'existe pas ...')
    except(ValueError):
        print('Merci de saisir un nombre ...')

def list_all(nb = 10):
    db = get_db()
    exec = db.execute("select distinct stop_name, stop_id from stops where location_type = '1' order by stop_name asc")
    print(f'Affichage des {nb} première gares :')
    stop_index = get_stop_index(clear = True)
    i = 0
    while (True):
        res = exec.fetchmany(nb)
        for r in res:
            stop_index[i] = r["stop_id"]
            print(f'- {r["stop_name"]} ({i})')            
            i += 1
        if input('Afficher plus ? (o/n)') != 'o':
            break

def list_search(stop):
    db = get_db()
    res = db.execute("select distinct stop_name, stop_id from stops where location_type = '1' and stop_name like ? order by stop_name asc",(f'%{stop}%',)).fetchall()
    stop_index = get_stop_index(clear = True)
    for i, r in enumerate(res):
        stop_index[i] = r["stop_id"]
        print(f'- {r["stop_name"]} ({i})')
  
# 0
print(time.strftime('%H:%M:%S') + 'db init ...')
db = get_db()
loader = core.SncfGtfsLoader(db)
loader.db_init()

# 1
print(time.strftime('%H:%M:%S') + 'load sources ...')
loader \
    .add_source('https://eu.ftp.opendatasoft.com/sncf/gtfs/export-ter-gtfs-last.zip') \
    .add_source('https://eu.ftp.opendatasoft.com/sncf/gtfs/export-intercites-gtfs-last.zip') \
    .add_source('https://eu.ftp.opendatasoft.com/sncf/gtfs/export_gtfs_voyages.zip')
loader.db_load()

# 2 
print(time.strftime('%H:%M:%S') + 'process trips ...')
process_trips()

# 3
print(time.strftime('%H:%M:%S') + 'done ! ready.')
list_search(input('Quelle gare souhaitez-vous chercher ?\n'))
get_trips_from(input('Quelle gare souhaitez-vous consulter ?\n'))
list_all()
get_trips_from(input('Quelle gare souhaitez-vous consulter ?\n'))

# à la fin
db.close()