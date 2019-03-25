from flask import Flask, jsonify, request
from os import path
import os
from flask_cors import CORS


cors = CORS()


# instantiate the app
app = Flask(__name__)
cors.init_app(app)


# set config
app_settings = os.getenv('APP_SETTINGS')
app.config.from_object(app_settings)


@app.route('/ping', methods=['GET'])
def ping_pong():
    return jsonify({
        'status': 'success',
        'message': 'pong!'
    })


@app.route('/data', methods=['POST'])
def add_data():
    post_data = request.get_json()

    app_path = post_data.get('appPath')
    root_path = path.abspath('../../')
    config_file_path = '%s/jupiter_config.py' % (root_path)
    modify_app_path_file(config_file_path, app_path)

    nodes_info = post_data.get('nodes')
    node_file_path = '%s/nodes.txt' % (root_path)
    modify_nodes_file(node_file_path, nodes_info)

    task_mapper_option = post_data.get('SCHEDULER')
    ini_file_path = '%s/jupiter_config.ini' % (root_path)
    modify_task_mapper_option(ini_file_path, task_mapper_option)

    response_object = {
        'status': 'success',
    }
    return jsonify(response_object), 201


def modify_app_path_file(file_path, app_path):
    with open(file_path, 'r+') as f:
        lines = f.readlines()
        count = 0
        for index, line in enumerate(lines):
            if(line.startswith('APP_NAME_INPUT') and count == 0):
                lines[index] = 'APP_NAME_INPUT = \'%s\'' % (app_path) + '\n'
                count += 1
    with open(file_path, 'w+') as f:
        for line in lines:
            f.write(line)
        f.close()


def modify_nodes_file(file_path, nodes_info):
    # node_num = nodes_info.get('nodesNum')
    node_details = nodes_info.get('nodesDetails')
    with open(file_path, 'w+') as f:
        f.write(node_details)
    with open(file_path, 'r+') as f:
        lines = f.readlines()
        for index, line in enumerate(lines):
            lines[index] = line.replace("\n", "") + ' root PASSWORD' + '\n'
    with open(file_path, 'w+') as f:
        for line in lines:
            f.write(line)
        f.close()


def modify_task_mapper_option(file_path, task_mapper_option):
    with open(file_path, 'r+') as f:
        lines = f.readlines()
        count = 0
        for index, line in enumerate(lines):
            if (line.startswith('    SCHEDULER') and count == 0):
                lines[index] = '    SCHEDULER = %s' % task_mapper_option + '\n'
                count += 1
    with open(file_path, 'w+') as f:
        for line in lines:
            f.write(line)
        f.close()
