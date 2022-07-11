from sys import prefix
from flask import (
    Blueprint, current_app, flash, g, make_response, redirect, render_template, request, url_for, jsonify
)
from werkzeug.exceptions import abort

from tchou.db import get_db

bp = Blueprint('search', __name__, url_prefix='/trips')

"""
@bp.route('/<stop_id>')
def get_stop(stop_id):
    db = get_db()
    res = db.execute('select type, src_name, tgt_name, min_time, max_time from times where src_id = ? order by tgt_name asc',(stop_id,))
    #print('De                   | Vers                 | Durée         | Type')
    #print('---------------------|----------------------|---------------|------------------')
    #for r in res:
        # print(f'{r["src_name"].ljust(20)} | {r["tgt_name"].ljust(20)} | {str(r["min_time"]).rjust(3)} - {str(r["max_time"]).rjust(3)} min | {re.findall("OCE[^-]*",r["type"])[0]}')
        #print(f'{r["src_name"].ljust(20)} | {r["tgt_name"].ljust(20)} | {str(r["min_time"]).rjust(3)} - {str(r["max_time"]).rjust(3)} min | {r["type"]}')
    resp = make_response(jsonify([dict(zip(row.keys(),tuple(row))) for row in res]))
    resp.headers['Access-Control-Allow-Origin'] = 'http://localhost:4200'
    return resp
    # return jsonify([dict(zip(row.keys(),tuple(row))) for row in res])
"""

@bp.route('/')
@bp.route('/<stop_id>')
def get_stop(stop_id = ""):
    db = get_db()
    with_coord = request.args.get('coord', False, type=bool)
    if with_coord:
        query="""
            select t.tgt_id, t.type, t.src_name, t.tgt_name, t.min_time, t.max_time,
            ss.stop_lon as src_lon, ss.stop_lat as src_lat, 
            st.stop_lon as tgt_lon, st.stop_lat as tgt_lat
            from times t
            join stops ss on t.src_id = ss.stop_id
            join stops st on t.tgt_id = st.stop_id
            where src_id = ? order by tgt_name asc;
        """
    else:
        query='select tgt_id, type, src_name, tgt_name, min_time, max_time from times where src_id = ? order by tgt_name asc'
    res = db.execute(query,(stop_id,))
    resp = make_response(jsonify([dict(zip(row.keys(),tuple(row))) for row in res]))
    resp.headers['Access-Control-Allow-Origin'] = current_app.config['ALLOW_ORIGIN']
    return resp
    # return jsonify([dict(zip(row.keys(),tuple(row))) for row in res])

@bp.route('/search/')
@bp.route('/search/<name_search>')
def search_stop(name_search = "IMPOSSIBLE A TROUVER"):
    db = get_db()
    res = db.execute("select distinct stop_id, stop_name, stop_lat, stop_lon from stops where location_type = '1' and stop_name like ? order by stop_name asc limit 5",(f'%{name_search}%',))
    resp = make_response(jsonify([dict(zip(row.keys(),tuple(row))) for row in res]))
    resp.headers['Access-Control-Allow-Origin'] = current_app.config['ALLOW_ORIGIN']
    return resp
    # return jsonify([dict(zip(row.keys(),tuple(row))) for row in res])
    
@bp.route('')
def list_all():
    db = get_db()
    query = "select distinct stop_name, stop_id from stops where location_type = '1' order by stop_name asc"
    cur = db.execute(query)
    page = request.args.get('page', 0, type=int)
    lines = max(min(request.args.get('lines', 10, type=int), 100), 10)
    if page > 0:
        page = max(min(page, (count_all() - 1) // lines), 0)
        print(f'{count_all()}')
        print(f'{page * lines}')
        cur.fetchmany(page * lines)   
    res = cur.fetchmany(lines)
    resp = make_response(jsonify([dict(zip(row.keys(),tuple(row))) for row in res]))
    resp.headers['Access-Control-Allow-Origin'] = current_app.config['ALLOW_ORIGIN'] #'http://localhost:4200'
    return resp
    # return jsonify([dict(zip(row.keys(),tuple(row))) for row in res])

def count_all():
    db = get_db()
    query = "select count(distinct stop_id) as count from stops where location_type = '1'"
    return db.execute(query).fetchone()['count']