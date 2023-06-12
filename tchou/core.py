#!python3

import csv
from datetime import datetime
import io
import sqlite3
from time import time
import zipfile
import requests

"""Core classes to be used with the webserver or terminal client"""

class SncfGtfsLoader:

    def __init__(self, db : sqlite3.Connection):
        self.db = db
        self.urls = []
    
    def add_source(self, url : str):
        self.urls.append(url)
        return self

    # 1. Load databases from SNCF public data (everyday refresh)
    def db_load(self):
        db = self.db        
        print(f'INSERT INTO properties (property, value) VALUES ("refresh_time", "{datetime.now().isoformat()}")')
        db.execute('INSERT INTO properties (property, value) VALUES (?, ?)',("refresh_time",datetime.now().isoformat()))
        for table in GtfsSchema.gtfs_schema:
            #print(f'delete from {table}')
            db.execute(f'DELETE FROM {table}')
        for url in self.urls:
            print('---- url ' + url + ' -----')
            resp = requests.get(url)
            with zipfile.ZipFile(io.BytesIO(resp.content),'r') as gtfs_archive:  
                for table, schema in GtfsSchema.gtfs_schema.items():
                    reader = csv.DictReader(io.TextIOWrapper(gtfs_archive.open(table + '.txt','r'),encoding='utf-8'))
                    fields = ', '.join(schema)
                    placeholders = ', '.join(f':{field}' for field in schema)
                    print(f'INSERT INTO {table} ({fields}) VALUES ({placeholders})')
                    db.executemany(f'INSERT INTO {table} ({fields}) VALUES ({placeholders})', reader )
                db.commit()
    
    def db_init(self):
        db = self.db
        print(f'db : {db}')
        for table, schema in GtfsSchema.gtfs_schema.items():
            fields = ", ".join(schema)
            print(f'DROP TABLE IF EXISTS {table};')
            db.execute(f'DROP TABLE IF EXISTS {table};')
            print(f'CREATE TABLE {table} ({fields})')
            db.execute(f'CREATE TABLE {table} ({fields})')
        # additional table properties to store custom values
        print(f'DROP TABLE IF EXISTS properties')
        db.execute(f'DROP TABLE IF EXISTS properties')        
        print(f'CREATE TABLE properties (property PRIMARY KEY, value)')
        db.execute(f'CREATE TABLE properties (property PRIMARY KEY, value)')
        db.commit()
    
class GtfsSchema:

    # not formal, TODO: check if the schema is well described ...
    gtfs_schema = {
        'agency': {
            'agency_id': str,
            'agency_name': str,
            'agency_url': str,
            'agency_timezone': str,
            'agency_lang': str,
        },
        'calendar_dates': {
            'service_id': int,
            'date': int,
            'exception_type': int,
        },
        'feed_info': {
            'feed_id': int,
            'feed_publisher_name': str,
            'feed_publisher_url': str,
            'feed_lang': str,
            'feed_start_date': int,
            'feed_end_date': int,
            'feed_version': str,
            'conv_rev': str,
            'plan_rev': str,
        },
        'routes': {
            'route_id': str,
            'agency_id': str,
            'route_short_name': str,
            'route_long_name': str,
            'route_desc': str,
            'route_type': int,
            'route_url': str,
            'route_color': str,
            'route_text_color': str,
        },
        'stop_times': {
            'trip_id': str,
            'arrival_time': time,
            'departure_time': time,
            'stop_id': str,
            'stop_sequence': int,
            'stop_headsign': str,
            'pickup_type': int,
            'drop_off_type': int,
            'shape_dist_traveled': str,
        },
        'stops': {
            'stop_id': str,
            'stop_name': str,
            'stop_desc': str,
            'stop_desc': float,
            'stop_lon': float,
            'stop_lat': float,
            'zone_id': str,
            'stop_url': str,
            'location_type': int,
            'parent_station': str,
        },
        'transfers': {
            'from_stop_id': str,
            'to_stop_id': str,
            'transfer_type': int,
            'min_transfer_time': int,
            'min_transfer_time': str,
            'to_route_id': str,
        },
        'trips': {
            'route_id': str,
            'service_id': int,
            'trip_id': str,
            'trip_headsign': int,
            'direction_id': int,
            'block_id': str,
            'shape_id': str
        }
    }

    def __init__(self):
        pass

    """
    tableA.col1 : a -> a[:3] 
    tableA.col2 : a -> idx[a]
    tableA.col3 : a -> a
    tableA.col4 : a -> None"""

class TripService:

    def __init__(self, db : sqlite3.Connection):
        self.db = db

    def generate_trips(self):
        db = self.db
        #   db.executescript(script.read())
        db.executescript("""
            create table if not exists times (type, src_id, tgt_id, src_name, tgt_name, min_time, max_time, min_stops, max_stops, total_trips);

            delete from times;

            insert into times 
            select
                replace(replace(s_src.stop_id,substr(s_src.stop_id,instr(s_src.stop_id,'-')),''),'StopPoint:',''),
                a_src.stop_id as 'from',
                a_trg.stop_id as 'to',
                a_src.stop_name as 'from_name',
                a_trg.stop_name as 'to_name',
                min((strftime('%s',st_trg.departure_time) - strftime('%s',st_src.arrival_time)) / 60) as 'min_time',
                max((strftime('%s',st_trg.departure_time) - strftime('%s',st_src.arrival_time)) / 60) as 'max_time',
                min(st_trg.stop_sequence - st_src.stop_sequence) as 'min_stops',
                max(st_trg.stop_sequence - st_src.stop_sequence) as 'max_stops',
                count(1) as 'total_trips'
            from stop_times st_src
            join stop_times st_trg on (st_src.trip_id = st_trg.trip_id and st_src.stop_id <> st_trg.stop_id and st_src.departure_time < st_trg.arrival_time)
            join stops s_src on st_src.stop_id = s_src.stop_id
            join stops s_trg on st_trg.stop_id = s_trg.stop_id
            join stops a_src on s_src.parent_station = a_src.stop_id
            join stops a_trg on s_trg.parent_station = a_trg.stop_id
            where s_src.location_type = '0' and st_src.stop_id not like 'StopPoint:OCECar TER%' -- exclure les trajets en CAR
            group by st_src.stop_id, st_trg.stop_id;
        """)
        db.commit()