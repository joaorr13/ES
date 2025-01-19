from flask import Blueprint, request, jsonify, make_response
from app.controllers.main import build_response
main = Blueprint('main', __name__)

@main.route('/')
def index():
    response = {
        "message": "Welcome to Facial Recognition Api"
    }
    return make_response(jsonify(response),200)


@main.route('/recognize', methods=['POST'])
def recognize():
    if request.method == 'POST':
        data = request.get_json()
        response = build_response( data["url"])
        
        return make_response(response, 200)
    else:
        return make_response('Method not allowed', 400)
