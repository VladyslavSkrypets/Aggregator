from flask import Blueprint, request, make_response, jsonify


admin = Blueprint('admin', __name__)


@admin.route('/login', methods=['POST'])
def admin_login():
    auth_data = request.json
    print(auth_data['name'], auth_data['password'])
    return make_response(jsonify({'message': 'admin data'}), 200)
