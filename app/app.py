import os

from flask import Flask
from . import db

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

if __name__ == '__main__':
    app.run()
