import json
from flask import Flask, make_response, render_template, request, jsonify
from . import db
from .db import add_kantor, get_count, get, get_all, delete, update, get_page

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
    
    add_kantor(data)

    return data, 200

@app.route('/api/lecturers', methods=['GET'] )
async def getalllec():
    return get_all()

@app.route('/api/lecturers/<lector_id>', methods=['GET'])
async def getlec(lector_id):
    data = get(lector_id)
    if data:
        return data, 200
    else:
        return make_response(jsonify({"status": "not found"}), 404)

@app.route('/api/lecturers/<lector_id>', methods=['DELETE'])
async def deletelec(lector_id):
    data = get(lector_id)
    if data:
        delete(lector_id)
        return {"status": "deleted"}, 200
    else:
        return {"status": "not found"}, 404

@app.route('/api/lecturers/<lector_id>', methods=['PUT'])
async def updatelec(lector_id):
    data = request.json
    message, status = get(lector_id)
    if status == 200:
        data, status = update(lector_id, data)
        return data, status
    else:
        return message, status
    
@app.route('/api/lecturers/main/<offset>', methods=['GET'])
async def getsixlec(offset):
    page, status = get_page(offset)
    return page, status

########### FrontEnd ###########

@app.route('/', methods=['GET'])
def main():
    data = get_all()
    count = get_count()
    return render_template("index.html", data = data, count = count)

@app.route('/lecturer')
def lecturer():
    with open("./app/data/lecturer.json", "r") as file:
        data = json.load(file)

    return render_template("lecturer.html", lecturer=data)

@app.route('/lecturer/<lector_id>', methods=['GET'])
def showlec(lector_id):
    data = get(lector_id)
    if data: 
        return render_template("lecturer.html", lecturer=data)
    else: 
        return render_template("404.html", lecturer=lector_id)


if __name__ == '__main__':
    app.run()
