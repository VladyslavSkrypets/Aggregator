from flask import Blueprint, make_response, jsonify


serp = Blueprint('serp', __name__)


@serp.route('/')
def serp_page():
    return make_response(jsonify({'message': 'Jobs page'}), 200)
