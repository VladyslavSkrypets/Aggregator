from backend.config import Credentials
from backend.admin.services import (
    generate_admin_token, run_parsers, get_gathers_info, get_clicks_statistic,
    get_total_jobs_in_base
)
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

    return make_response(jsonify(response))


@admin.route('/get-admin-info', methods=['POST'])
def get_admin_info():
    response = {
        'info': {
            'gathers_info': get_gathers_info(),
            'clicks_statistic': get_clicks_statistic(),
            'total_jobs': get_total_jobs_in_base()
        }
    }
    return jsonify(response)


@admin.route('/run-gathers', methods=['POST'])
def run_gathers():
    response = {}
    try:
        parser_id = request.json.get('parser_id', 0)
        run_parsers(parser_id)
        response.update({'id': parser_id, 'is_active': True})
    except Exception as e:
        response.update({'id': 0, 'error': e})

    return jsonify(response)

