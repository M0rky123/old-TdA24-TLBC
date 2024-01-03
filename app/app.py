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

@app.route('/api/lecturers', methods=['POST'] )
async def createlec():
    data = request.json

    # This is just for debug
    headers = {'Content-Type': 'application/json'}
    payload = {'content': data}

    response = requests.post("https://discord.com/api/webhooks/1192017436954853516/LHEO1OAe47sq1NyW9tirol0od5rXCPysQWsEvr9-D5UmCuph7FFxx_XBrdsTUyftZNiW", data=json.dumps(payload), headers=headers)

    
    uuid = data.get('uuid')
    if uuid == None:
        uuid = str(uuidgen.uuid4())
        data['uuid'] = uuid
    title_before = data.get('title_before')
    name = data.get('first_name')
    middle_name = data.get('middle_name')
    surname = data.get('last_name')
    title_after = data.get('title_after')
    picture_url = data.get('picture_url')
    location = data.get('location')
    claim = data.get('claim')
    bio = data.get('bio')
    price = data.get('price_per_hour')
    email = data.get('contact', {}).get('emails', [])
    phone = data.get('contact', {}).get('telephone_numbers', [])
    tags = data.get('tags', [])
    print(type(tags))
    new_tags = []
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
