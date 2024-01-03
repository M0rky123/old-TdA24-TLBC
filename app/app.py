import os
import json
import requests
from flask import Flask, render_template, request, jsonify
from . import db
from .db import add_kantor, select_kantor, get_all_tags, add_tag_to_db, select_all_kantori, create_tag_if_not_exist
import uuid as uuidgen

logo = "./static/img/logo_white.png"

template = "./app/index.html"

app = Flask(__name__, static_folder="static")
app.config['DATABASE'] = './app/data/lecture.db'
app.json.sort_keys = False

db.init_app(app)


#@app.route('/')
#def hello_world():
#    return "Hello TdA"

@app.route('/api')
def api():
    return {"secret":"The cake is a lie"}


########### API ###########

def process_field(data, field_name, default_value=None):
    field_value = data.get(field_name)
    if field_value is None:
        field_value = default_value
    elif field_value == "":
        field_value = None

    return field_value

@app.route('/api/lecturers', methods=['POST'] )
async def createlec():
    data = request.json

    # UUID Generation
    uuid = data.get('uuid') or str(uuidgen.uuid4())
    data['uuid'] = uuid

    title_before = process_field(data, 'title_before')
    name = process_field(data, 'first_name')
    middle_name = process_field(data, 'middle_name')
    last_name = process_field(data, 'last_name')
    title_after = process_field(data, 'title_after')
    picture_url = process_field(data, 'picture_url')
    location = process_field(data, 'location')
    claim = process_field(data, 'claim')
    bio = process_field(data, 'bio')
    price = process_field(data, 'price_per_hour')
    tags = data.get('tags', [])
    new_tags = []

    if not name or not last_name:
        return {"error": "Missing mandatory fields: 'first_name' or 'last_name'"}, 400

    contact_info = data.get('contact', {})
    emails = contact_info.get('emails', [])
    telephone_numbers = contact_info.get('telephone_numbers', [])

    for tag in tags:
        if isinstance(tag, dict):
            tag_name = tag.pop("name", None)
            if tag_name:
                new_tag = create_tag_if_not_exist(tag_name)
                new_tags.append(new_tag)
    tags = new_tags
    data['tags'] = tags
        
    add_kantor(title_before, name, middle_name, surname, picture_url, title_after, price, location, claim, bio, uuid, email, phone, tags)

    print(data)
    return data, 200

@app.route('/api/lecturers', methods=['GET'] )
async def getalllec():
    return select_all_kantori()

@app.route('/add_tag', methods=['GET', 'POST'])
def add_tag():
    if request.method == 'POST':
        tag_name = request.form['tag_name']
        tag_id = request.form['tag_id']

        add_tag_to_db(tag_name, tag_id)
    
    return render_template('add_tag.html')



@app.route('/add', methods=['GET', 'POST'])
def add():
    if request.method == 'POST':
        title_before = request.form['title_before']
        name = request.form['name']
        middle_name = request.form['middle_name']
        surname = request.form['surname']
        title_after = request.form['title_after']
        picture_url = request.form['picture_url']
        price = request.form['price']
        location = request.form['location']
        claim = request.form['claim']
        bio = request.form['bio']
        email = request.form['email']
        phone = request.form['phone']
        tags = request.form.getlist('option')  # Assuming 'item' is a list in the form


        items.extend(tags)
        print(items)
        add_kantor(title_before, name, middle_name, surname, picture_url, title_after, price, location, claim, bio, email, phone, items)

    existing_tags = get_all_tags()
    return render_template('add_kantor.html', existing_tags=existing_tags)

items = []
@app.route('/add_item', methods=['POST'])
def add_item():
    item = request.json['item']
    
    items.append(item)
    return jsonify(items=items)

@app.route('/api/lecturers/<lector_id>', methods=['GET'] )
def getlector(lector_id):
    data = select_kantor(lector_id)
    return data


########### FrontEnd ###########

@app.route('/', methods=['GET'])
def main():
    return render_template("index.html")

@app.route('/lecturer')
def lecturer():
    with open("./app/data/lecturer.json", "r") as file:
        data = json.load(file)

    return render_template("lecturer.html", lecturer=data, logoing=logo)

@app.route('/lecturer/<lector_id>', methods=['GET'])
def showlec(lector_id):
    data = getlector(lector_id)
    if data: 
        return render_template("lecturer-template.html", lecturer=data)
    else: 
        return render_template("404.html", lecturer=lector_id)



if __name__ == '__main__':
    app.run()
