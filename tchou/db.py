import os
import sqlite3

import click
from flask import current_app, g
from flask.cli import with_appcontext

import tchou.ressources.gtfs_loader # TODO: should be relative to root path

def get_db(force_create = False):
    if 'db' not in g:
        if os.path.isfile(current_app.config['DATABASE']) or force_create:
            g.db = sqlite3.connect(
                current_app.config['DATABASE'],
                detect_types=sqlite3.PARSE_DECLTYPES
            )
            g.db.row_factory = sqlite3.Row
        else: 
            raise ConnectionError('Database does not exists')
    return g.db

def close_db(e=None):
    db = g.pop('db', None)
    if db is not None:
        db.close()

@click.command('db:init')
@with_appcontext
def db_init():
    """Clear the existing data and create new tables."""
    db = get_db(force_create=True)
    loader = tchou.ressources.gtfs_loader.SncfGtfsLoader(db)
    loader.db_init()
    click.echo('Initialized the database.')

@click.command('db:load-data')
@with_appcontext
def db_load_data():
    """Clear the existing data and create new tables."""
    db = get_db()
    loader = tchou.ressources.gtfs_loader.SncfGtfsLoader(db)
    loader \
        .add_source('https://eu.ftp.opendatasoft.com/sncf/gtfs/export-ter-gtfs-last.zip') \
        .add_source('https://eu.ftp.opendatasoft.com/sncf/gtfs/export-intercites-gtfs-last.zip') \
        .add_source('https://eu.ftp.opendatasoft.com/sncf/gtfs/export_gtfs_voyages.zip')
    loader.db_load()
    click.echo('Sncf data loaded.')

@click.command('db:generate-trips')
@with_appcontext
def db_generate_trips():
    """Clear the existing data and create new tables."""
    db = get_db()
    trip_service = tchou.ressources.gtfs_loader.TripService(db)
    trip_service.generate_trips()
    click.echo('Trips generated.')

def init_app(app):
    app.teardown_appcontext(close_db)
    app.cli.add_command(db_init)
    app.cli.add_command(db_load_data)
    app.cli.add_command(db_generate_trips)