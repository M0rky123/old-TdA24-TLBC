import click
from flask import Flask, current_app, g
from flask.cli import with_appcontext
import sqlite3
import uuid



CREATE_KATEGORIE_TABLE = """
CREATE TABLE IF NOT EXISTS kategorie (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  name TEXT NOT NULL
);
"""

CREATE_KANTORI_TABLE = """
CREATE TABLE IF NOT EXISTS kantori (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  _uuid TEXT,
  _title_before TEXT,
  _name TEXT NOT NULL,
  _middle_name TEXT,
  _surname TEXT NOT NULL,
  _title_after TEXT,
  _location TEXT,
  _claim TEXT,
  _bio TEXT,
  _email TEXT NOT NULL,
  _phone INTEGER NOT NULL,
  _tags TEXT
);
"""

INIT_DB_STATEMENTS = [CREATE_KATEGORIE_TABLE, CREATE_KANTORI_TABLE]

def get_db():
    if 'db' not in g:
        g.db = sqlite3.connect(
            current_app.config['DATABASE'],
            detect_types=sqlite3.PARSE_DECLTYPES
        )
        g.db.row_factory = sqlite3.Row
    return g.db

def close_db(e=None):
    db = g.pop('db', None)
    if db is not None:
        db.close()

def init_db():
    with get_db() as db:
        for statement in INIT_DB_STATEMENTS:
            db.executescript(statement)

@click.command('init-db')
@with_appcontext
def init_db_command():
    """
    Definujeme příkaz příkazové řádky
    """
    init_db()
    click.echo('Initialized the database.')


def init_app(app):
    app.teardown_appcontext(close_db)
    app.cli.add_command(init_db_command)

def select_all_kantori():
    with sqlite3.connect(current_app.config['DATABASE']) as connection:
        cursor = connection.cursor()
        cursor.execute("SELECT * FROM kantori")
        return cursor.fetchall()


def select_kantor(uuid):
    with sqlite3.connect(current_app.config['DATABASE']) as connection:
        cursor = connection.cursor()
        cursor.execute("SELECT * FROM kantori WHERE _uuid = ?", (uuid,))
        return cursor.fetchone()
    
def add_kantor(title_before: None, name, middle_name: None, surname, title_after: None, location: None, claim: None, bio: None, email, phone = int, tags: None = list):
    kantor_id = uuid.uuid4()
    taglist = str(tags)
    with sqlite3.connect(current_app.config['DATABASE']) as connection:
        cursor = connection.cursor()
        cursor.execute("INSERT INTO kantori (_title_before, _name, _middle_name, _surname, _title_after, _location, _claim, _bio, _email, _phone, _uuid, _tags) VALUES (?,?,?,?,?,?,?,?,?,?,?,?)", (title_before, name, middle_name, surname, title_after, location, claim, bio, email, phone, str(kantor_id), taglist))
        
    connection.commit()

@click.command('init-db')
@with_appcontext
def init_db_command():
    init_db()
    click.echo('Initialized the database.')

def init_app(app):
    app.teardown_appcontext(close_db)
    app.cli.add_command(init_db_command)


