import os
import json
from flask import Flask, render_template
from . import db

template = "./app/index.html"

app = Flask(__name__)

app.config.from_mapping(
    DATABASE=os.path.join(app.instance_path, 'tourdeflask.sqlite'),
)

try:
    os.makedirs(app.instance_path)
except OSError:
    pass

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

@app.route('/api/lecturers/<lector_id>', methods=['GET'] )
async def getlec():
    pass



if __name__ == '__main__':
    app.run()
