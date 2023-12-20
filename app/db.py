import click
from flask import Flask, current_app, g
from flask.cli import with_appcontext
import sqlite3
import uuid



CREATE_TAG_TABLE = """
CREATE TABLE IF NOT EXISTS tags (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  tag_name TEXT NOT NULL,
  tag_id TEXT NOT NULL
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
  price INTEGER,
  loc TEXT,
  claim TEXT,
  bio TEXT,
  email TEXT NOT NULL,
  phone INTEGER NOT NULL,
  tags TEXT
);
"""

INIT_DB_STATEMENTS = [CREATE_TAG_TABLE, CREATE_KANTORI_TABLE]

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
    
def add_kantor(title_before: None, name, middle_name: None, surname, picture_url: None, title_after: None, price: None, location: None, claim: None, bio: None, email, phone = int, tags: None = list):
    kantor_id = str(uuid.uuid4())
    taglist = str(["Not", "Working", "YET"])
    print(type(phone))
    with sqlite3.connect(current_app.config['DATABASE']) as connection:
        cursor = connection.cursor()
        cursor.execute("INSERT INTO kantori (title_before, first_name, middle_name, surname, picture_url, title_after, price, loc, claim, bio, email, phone, uuid, tags) VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?,?)", (title_before, name, middle_name, surname, picture_url, title_after, price, location, claim, bio, email, int(phone), kantor_id, taglist))
        
    connection.commit()

def add_tag_to_db(name, uuid: None):
    if uuid == None:
        uuid = str(uuid.uuid4())
    with sqlite3.connect(current_app.config['DATABASE']) as connection:
        cursor = connection.cursor()
        cursor.execute("INSERT INTO tags (tag_name, tag_id) VALUES (?, ?)", (name, uuid))

    connection.commit()

def get_all_tags():
    with sqlite3.connect(current_app.config['DATABASE']) as connection:
        cursor = connection.cursor()
        cursor.execute("SELECT * FROM tags")
        return cursor.fetchall()

@click.command('init-db')
@with_appcontext
def init_db_command():
    init_db()
    click.echo('Initialized the database.')

def init_app(app):
    app.teardown_appcontext(close_db)
    app.cli.add_command(init_db_command)


