import click
from flask import Flask, current_app, g, abort
from flask.cli import with_appcontext
import sqlite3
import uuid as uuidgen



CREATE_TAG_TABLE = """
CREATE TABLE IF NOT EXISTS tags (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  tag_name TEXT NOT NULL,
  tag_id TEXT NOT NULL
);
"""

CREATE_KANTORI_TABLE = """
CREATE TABLE IF NOT EXISTS kantori (
  uuid TEXT,
  title_before TEXT,
  first_name TEXT NOT NULL,
  middle_name TEXT,
  last_name TEXT NOT NULL,
  title_after TEXT,
  picture_url TEXT,
  price INTEGER,
  location TEXT,
  claim TEXT,
  bio TEXT,
  email TEXT NOT NULL,
  phone TEXT NOT NULL,
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

def dict_factory(cursor, row):
    d = {}
    for idx, col in enumerate(cursor.description):
        d[col[0]] = row[idx]
    return d

def select_all_kantori():
    with sqlite3.connect(current_app.config['DATABASE']) as connection:
        connection.row_factory = dict_factory
        cursor = connection.cursor()
        cursor.execute("SELECT * FROM kantori")
        data = cursor.fetchall()
        for lector in data:
            lector.pop("id", None)
            lector["uuid"] = lector.pop("uuid", None)
            lector["last_name"] = lector.pop("last_name", None)
            lector["picture_url"] = lector.pop("picture_url", None)
            lector["location"] = lector.pop("location", None)
            lector["claim"] = lector.pop("claim", None)
            lector["bio"] = lector.pop("bio", None)
            lector["tags"] = eval(lector.pop("tags", None))
            lector["price_per_hour"] = lector.pop("price", None)
            lector["contact"] = {
                "telephone_numbers": eval(lector.pop("phone", [])),
                "emails": eval(lector.pop("email", []))
            }

            for key in lector.keys():
                if lector[key] is None:
                    lector[key] = ""
        return data

def select_kantori_by_key(parsed_key, limit=6):
    offset = (int(parsed_key) - 1) * limit

    with sqlite3.connect(current_app.config['DATABASE']) as connection:
        connection.row_factory = dict_factory
        cursor = connection.cursor()
        
        cursor.execute(f"SELECT * FROM kantori LIMIT {limit} OFFSET {offset}")
        data = cursor.fetchall()
        lecturers = []
        for lector in data:
            lector.pop("id", None)
            lector["uuid"] = lector.pop("uuid", None)
            lector["last_name"] = lector.pop("last_name", None)
            lector["picture_url"] = lector.pop("picture_url", None)
            lector["location"] = lector.pop("location", None)
            lector["claim"] = lector.pop("claim", None)
            lector["bio"] = lector.pop("bio", None)
            lector["tags"] = eval(lector.pop("tags", None))
            lector["price_per_hour"] = lector.pop("price", None)
            lector["contact"] = {
                "telephone_numbers": eval(lector.pop("phone", [])),
                "emails": eval(lector.pop("email", []))
            }

            for key in lector.keys():
                if lector[key] is None:
                    lector[key] = ""
            lecturers.append(lector)

        return lecturers

def select_kantor(uuid):
    with sqlite3.connect(current_app.config['DATABASE']) as connection:
        connection.row_factory = dict_factory
        cursor = connection.cursor()
        cursor.execute("SELECT * FROM kantori WHERE uuid = ?", (uuid,))
        data = cursor.fetchone()
        if data:
            data["price_per_hour"] = data.pop("price", None)
            data["tags"] = eval(data["tags"])
            data["contact"] = {
                "telephone_numbers": eval(data.pop("phone", [])),
                "emails": eval(data.pop("email", []))
            }
            return data
        else: 
            abort(404)

def update_kantor(uuid, data):
    with sqlite3.connect(current_app.config['DATABASE']) as connection:
        connection.row_factory = sqlite3.Row
        cursor = connection.cursor()


        cursor.execute("SELECT COUNT(*) FROM kantori WHERE uuid = ?", (uuid,))
        lector_exists = cursor.fetchone()

        if lector_exists:
            for key in data.keys():
                if data[key] is None:
                    data[key] = ""
            cursor.execute("DELETE FROM kantori WHERE uuid = ?", (uuid,))
            cursor.execute("INSERT INTO kantori (title_before, first_name, middle_name, last_name, picture_url, title_after, price, location, claim, bio, email, phone, uuid, tags) VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?,?)", (data["title_before"], data["first_name"], data["middle_name"], data["last_name"], data["picture_url"], data["title_after"], data["price_per_hour"], data["location"], data["claim"], data["bio"], str(data["contact"]["emails"]), str(data["contact"]["telephone_numbers"]), str(uuid), str(data["tags"])))
            data["uuid"] = uuid
            connection.commit()
            new_tags = []
            tags = data["tags"]
            for tag in tags:
                if isinstance(tag, dict):
                    tag_name = tag.pop("name", None)
                    if tag_name:
                        new_tag = create_tag_if_not_exist(tag_name)
                        new_tags.append(new_tag)
            tags = new_tags
            data['tags'] = tags

            return data, 200
        else:
            return {"status": "not found"}, 404

def delete_kantor(uuid):
    with sqlite3.connect(current_app.config['DATABASE']) as connection:
        cursor = connection.cursor()
        cursor.execute("DELETE FROM kantori WHERE uuid = ?", (uuid,))
        connection.commit()

def create_tag_if_not_exist(tag_name):
    with sqlite3.connect(current_app.config['DATABASE']) as connection:
        cursor = connection.cursor()
        cursor.execute("SELECT * FROM tags WHERE tag_name = ?", (tag_name,))

        data = cursor.fetchone()
        if data:
            data = {"name": data[1], "uuid": data[2]}
            return data
        else:
            data = add_tag_to_db(tag_name)
            return data
   
def add_kantor(title_before: None, name, middle_name: None, last_name, picture_url: None, title_after: None, price: None, location: None, claim: None, bio: None, uuid = str, email = list, phone = list, tags: None = list):
    with sqlite3.connect(current_app.config['DATABASE']) as connection:
        cursor = connection.cursor()
        cursor.execute("INSERT INTO kantori (title_before, first_name, middle_name, last_name, picture_url, title_after, price, location, claim, bio, email, phone, uuid, tags) VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?,?)", (title_before, name, middle_name, last_name, picture_url, title_after, price, location, claim, bio, str(email), str(phone), str(uuid), str(tags)))
        
    connection.commit()

def add_tag_to_db(name):
    uuid = str(uuidgen.uuid4())
    with sqlite3.connect(current_app.config['DATABASE']) as connection:
        cursor = connection.cursor()
        cursor.execute("INSERT INTO tags (tag_name, tag_id) VALUES (?, ?)", (name, uuid))

    connection.commit()
    return {"name": name, "uuid": uuid}

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


