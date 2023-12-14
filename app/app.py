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
    return "Hello TdA - test"

@app.route('/api')
def api():
    return {"secret":"The cake is a lie"}

@app.route('/lecturer')
def lecturer():
    #data = {'name': 'John', 'age': 25}
    with open("./data/lecturer.json", "r") as file:
        data = json.load(file)

    return render_template("lecturer.html", lecturer=data)


if __name__ == '__main__':
    app.run()
