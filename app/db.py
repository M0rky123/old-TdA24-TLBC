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
  uuid TEXT,
  title_before TEXT,
  first_name TEXT NOT NULL,
  middle_name TEXT,
  surname TEXT NOT NULL,
  picture_url TEXT,
  title_after TEXT,
  loc TEXT,
  claim TEXT,
  bio TEXT,
  email TEXT NOT NULL,
  phone INTEGER NOT NULL,
  tags TEXT
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


def dict_factory(cursor, row):
    d = {}
    for idx, col in enumerate(cursor.description):
        d[col[0]] = row[idx]
    return d

def select_kantor(uuid):
    with sqlite3.connect(current_app.config['DATABASE']) as connection:
        connection.row_factory = dict_factory
        cursor = connection.cursor()
        cursor.execute("SELECT * FROM kantori WHERE uuid = ?", (uuid,))
        return cursor.fetchone()
    
def add_kantor(title_before: None, name, middle_name: None, surname, picture_url, title_after: None, location: None, claim: None, bio: None, email, phone = int, tags: None = list):
    kantor_id = uuid.uuid4()
    taglist = str(tags)
    with sqlite3.connect(current_app.config['DATABASE']) as connection:
        cursor = connection.cursor()
        cursor.execute("INSERT INTO kantori (title_before, first_name, middle_name, surname, picture_url, title_after, loc, claim, bio, email, phone, uuid, tags) VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?)", (title_before, name, middle_name, surname, picture_url, title_after, location, claim, bio, email, phone, str(kantor_id), taglist))
        
    connection.commit()

@click.command('init-db')
@with_appcontext
def init_db_command():
    init_db()
    click.echo('Initialized the database.')

def init_app(app):
    app.teardown_appcontext(close_db)
    app.cli.add_command(init_db_command)


