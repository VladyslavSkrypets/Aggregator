from backend.config import Credentials
from backend.admin.services import generate_admin_token
from flask import Blueprint, request, make_response, jsonify


admin = Blueprint('admin', __name__)


@admin.route('/login', methods=['POST'])
def admin_login():
    response = {}
    auth_data = request.json
    username_incorrect = auth_data['username'] != Credentials.USERNAME
    password_incorrect = auth_data['password'] != Credentials.PASSWORD
    error_messages = {
        'Incorrect username': username_incorrect,
        'Incorrect password': password_incorrect
    }

    if any(error_messages.values()):
        response.update({
                'message': '\n'.join(
                    [message for message in error_messages if error_messages[message]]
                ),
                'status': 401
        })
    else:
        response.update({
            'message': 'success',
            'token': generate_admin_token(),
            'status': 200
        })

    return make_response(jsonify(response), response['status'])
