import os
import json
import requests
from flask import Flask, render_template, request, jsonify
from . import db
from .db import add_kantor, select_kantor, get_all_tags, add_tag_to_db

logo = "./static/img/logo_white.png"

template = "./app/index.html"

app = Flask(__name__, static_folder="static")
app.config['DATABASE'] = './app/data/lecture.db'

db.init_app(app)


@app.route('/')
def hello_world():
    return "Hello TdA"

@app.route('/api')
def api():
    return {"secret":"The cake is a lie"}

@app.route('/lecturer')
def lecturer():
    #data = {'name': 'John', 'age': 25}
    with open("./app/data/lecturer.json", "r") as file:
        data = json.load(file)

    return render_template("lecturer.html", lecturer=data, logoing=logo)

@app.route('/api/lecturers', methods=['POST'] )
async def createlec():
    pass

@app.route('/api/lecturers', methods=['GET'] )
async def getalllec():
    pass

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
async def getlec(lector_id):
    data = select_kantor(lector_id)
    if data: 
        return render_template("lecturer-template.html", lecturer=data)
    else: 
        return render_template("404.html", lecturer=lector_id)



if __name__ == '__main__':
    app.run()
