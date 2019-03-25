from flask import Blueprint, jsonify


backend_blueprint = Blueprint('backend', __name__)


@backend_blueprint.route('/ping', methods=['GET'])
def ping_pong():
    return jsonify({
        'status': 'success',
        'message': 'pong!'
    })