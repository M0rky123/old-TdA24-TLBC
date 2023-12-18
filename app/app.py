import os
import json
import requests
from flask import Flask, render_template, request, jsonify
from . import db
from .db import add_kantor, select_kantor

template = "./app/index.html"

app = Flask(__name__)
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

    return render_template("lecturer.html", lecturer=data)

@app.route('/api/lecturers', methods=['POST'] )
async def createlec():
    pass

@app.route('/api/lecturers', methods=['GET'] )
async def getalllec():
    pass

@app.route('/add', methods=['GET', 'POST'])
def add():
    if request.method == 'POST':
        title_before = request.form['title_before']
        name = request.form['name']
        middle_name = request.form['middle_name']
        surname = request.form['surname']
        title_after = request.form['title_after']
        location = request.form['location']
        claim = request.form['claim']
        bio = request.form['bio']
        email = request.form['email']
        phone = request.form['phone']

        add_kantor(title_before, name, middle_name, surname, title_after, location, claim, bio, email, phone)

    return render_template('add_kantor.html')

@app.route('/api/lecturers/<lector_id>', methods=['GET'] )
async def getlec(lector_id):
    data = select_kantor(lector_id)
    return (jsonify(data))



if __name__ == '__main__':
    app.run()
