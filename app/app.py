import os
import json
import requests
from flask import Flask, make_response, render_template, request, jsonify
from . import db
from .db import add_kantor, lector_count, select_kantor, get_all_tags, add_tag_to_db, select_all_kantori, create_tag_if_not_exist, delete_kantor, update_kantor,select_kantori_by_key
import uuid as uuidgen

logo = "./static/img/logo_white.png"

template = "./app/index.html"

app = Flask(__name__, static_folder="static")
app.config['DATABASE'] = './app/data/lecture.db'
app.json.sort_keys = False

db.init_app(app)

######## Fáze 1 ########

#@app.route('/')
#def hello_world():
#    return "Hello TdA"

@app.route('/api')
def api():
    return {"secret":"The cake is a lie"}

def validate_required_fields(data):
    required_fields = ['first_name', 'last_name', 'contact']
    for field in required_fields:
        if data.get(field) is None:
            return False
    contact_info = data.get('contact', {})
    if not contact_info.get('emails') or not contact_info.get('telephone_numbers'):
        return False
    return True


########### API ###########



@app.route('/api/lecturers', methods=['POST'] )
async def createlec():
    data = request.json

    if not validate_required_fields(data):
        return jsonify({"error": "Missing required fields"}), 400
    
    uuid = data.get('uuid')
    if not uuid:
        uuid = str(uuidgen.uuid4())
        data['uuid'] = uuid
    title_before = data.get('title_before')
    name = data.get('first_name')
    middle_name = data.get('middle_name')
    last_name = data.get('last_name')
    title_after = data.get('title_after')
    picture_url = data.get('picture_url')
    location = data.get('location')
    claim = data.get('claim')
    bio = data.get('bio')
    price = data.get('price_per_hour')
    email = data.get('contact', {}).get('emails', [])
    phone = data.get('contact', {}).get('telephone_numbers', [])
    tags = data.get('tags', [])
    new_tags = []
    for tag in tags:
        if isinstance(tag, dict):
            tag_name = tag.pop("name", None)
            if tag_name:
                new_tag = create_tag_if_not_exist(tag_name)
                new_tags.append(new_tag)
    tags = new_tags
    data['tags'] = tags
        
    add_kantor(title_before=title_before, first_name=name, middle_name=middle_name, last_name=last_name, picture_url=picture_url, title_after=title_after, price=price, location=location, claim=claim, bio=bio, uuid=uuid, email=email, phone=phone, tags=tags)

    return data, 200

@app.route('/api/lecturers', methods=['GET'] )
async def getalllec():
    return select_all_kantori()

@app.route('/api/lecturers/<lector_id>', methods=['GET'])
async def getlec(lector_id):
    data = select_kantor(lector_id)
    if data:
        return data, 200
    else:
        return make_response(jsonify({"status": "not found"}), 404)

@app.route('/api/lecturers/<lector_id>', methods=['DELETE'])
async def deletelec(lector_id):
    data = select_kantor(lector_id)
    if data:
        delete_kantor(lector_id)
        return {"status": "deleted"}, 200
    else:
        return {"status": "not found"}, 404

@app.route('/api/lecturers/<lector_id>', methods=['PUT'])
async def updatelec(lector_id):
    data = request.json
    if data:
        update_kantor(lector_id, data)
        return {"status": "updated"}, 200
    else:
        return {"status": "not found"}, 404
    
@app.route('/api/lecturers/main/<offset>', methods=['GET'])
async def getsixlec(offset):
    data = select_kantori_by_key(offset)
    if data:
        return data, 200


########### FrontEnd ###########

@app.route('/', methods=['GET'])
def main():
    data = select_all_kantori()
    count = lector_count()
    print(count)
    return render_template("index.html", data = data, count = count)

@app.route('/lecturer')
def lecturer():
    with open("./app/data/lecturer.json", "r") as file:
        data = json.load(file)

    return render_template("lecturer.html", lecturer=data, logoing=logo)

@app.route('/lecturer/<lector_id>', methods=['GET'])
def showlec(lector_id):
    data = select_kantor(lector_id)
    if data: 
        return render_template("lecturer.html", lecturer=data)
    else: 
        return render_template("404.html", lecturer=lector_id)



if __name__ == '__main__':
    app.run()
