import sqlite3
import click

from flask import current_app, g
from flask.cli import with_appcontext

def get_db():
    #g is a special object that is unique in each request. It is used to store data that may be accessed by 
    #multiple functions during the request
    if 'db' not in g:
        #current_App is another special object that points to the flask app handling the request
        #sqlite3.connect establishes a connection to the file pointed at by the database. The file doesnt have to exist yet
        g.db = sqlite3.connect(
            current_app.config['DATABASE'],
            detect_types=sqlite3.PARSE_DECLTYPES
        )
        #sqlite3.Row tells the connection to return rows that behave like dicts. This allows accessing columns by name
        g.db.row_fatory = sqlite3.Row
    return g.db

#close_db checks if connection was created by checking if g.db was set. If the connetion exists,it is closed
def close_db(e=None):
    db = g.pop('db', None)
    if db is not None:
        db.close() 

#Add python functions to run the sql file
def init_db():
    db = get_db()
    #open_resource opens a file relative to flaskr package
    with current_app.open_resource('schema.sql') as f:
        db.executescript(f.read().decode('utf8'))

#click.command defines a command line called init_db that calls the init_db function and shows a success message to user
@click.command('init-db')
@with_appcontext
def init_db_command():
    """Clear the existing data and create new tables."""
    init_db()
    click.echo('initialized the database.')

#To register close_db and init_db command functions on applicaation
def init_app(app):
    app.teardown_appcontext(close_db)
    app.cli.add_command(init_db_command)
#app.teardown_appcontext tells flask to call that function when cleaning up after returning the response
#app.cli.add_command adds a new command that can be called with the flask command