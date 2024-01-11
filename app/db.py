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
            return None

def lector_count():
    with sqlite3.connect(current_app.config['DATABASE']) as connection:
        cursor = connection.cursor()
        cursor.execute("SELECT COUNT(*) FROM kantori")
        data = cursor.fetchone()
        return data[0]

import sqlite3
from flask import current_app

import sqlite3
from flask import current_app

def update_kantor(uuid, kantor_data):
    with sqlite3.connect(current_app.config['DATABASE']) as connection:
        cursor = connection.cursor()

        # Fetch existing data to update selectively
        cursor.execute("SELECT * FROM kantori WHERE uuid=?", (str(uuid),))
        existing_data = cursor.fetchone()

        if existing_data:
            # Create a dictionary to store updated values
            updated_values = {}

            # Iterate through the keys in the JSON data
            for key in kantor_data.keys():
                # Check if the key exists in the database table
                if key in ['title_before', 'first_name', 'middle_name', 'last_name', 'picture_url', 'title_after', 'price', 'location', 'claim', 'bio', 'email', 'phone', 'tags']:
                    if key == 'tags':
                        # Extract tag names from nested structure
                        tags = str(kantor_data["tags"])
                        updated_values['tags'] = tags
                    elif key == 'contact':
                        # Extract phone and email information from nested structure
                        if 'telephone_numbers' in kantor_data[key]:
                            updated_values['phone'] = ', '.join(kantor_data[key]['telephone_numbers'])
                        if 'emails' in kantor_data[key]:
                            updated_values['email'] = ', '.join(kantor_data[key]['emails'])
                    else:
                        updated_values[key] = kantor_data[key]

            # Generate SQL UPDATE query
            update_query = "UPDATE kantori SET "
            update_values = []

            for key, value in updated_values.items():
                update_query += f"{key}=?, "
                update_values.append(value)

            update_query = update_query.rstrip(', ')  # Remove the trailing comma
            update_query += " WHERE uuid=?"

            # Add the UUID to the update values
            update_values.append(str(uuid))

            # Execute the update query
            cursor.execute(update_query, tuple(update_values))

            connection.commit()
            data = select_kantor(uuid)
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
   
def add_kantor(title_before: None, first_name, middle_name: None, last_name, picture_url: None, title_after: None, price: None, location: None, claim: None, bio: None, uuid = str, email = list, phone = list, tags: None = list):
    with sqlite3.connect(current_app.config['DATABASE']) as connection:
        cursor = connection.cursor()
        cursor.execute("INSERT INTO kantori (title_before, first_name, middle_name, last_name, picture_url, title_after, price, location, claim, bio, email, phone, uuid, tags) VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?,?)", (title_before, first_name, middle_name, last_name, picture_url, title_after, price, location, claim, bio, str(email), str(phone), str(uuid), str(tags)))
        
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


