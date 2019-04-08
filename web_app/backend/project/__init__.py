from flask import Flask, jsonify, request
from os import path
import os
from flask_cors import CORS
import json
import time

import subprocess
import sys
sys.path.append(path.abspath(__file__ + "/../../../../"))
import jupiter_config


cors = CORS()


# instantiate the app
app = Flask(__name__)
cors.init_app(app)


# set config
app_settings = os.getenv('APP_SETTINGS')
app.config.from_object(app_settings)


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


@app.route('/run_exec_profiler', methods=['POST'])
def get_exec_profile_info():
    jupiter_config.set_globals()
    exec_namespace = jupiter_config.EXEC_NAMESPACE
    app_name = jupiter_config.APP_OPTION
    cmd = "kubectl get pod -l app=%s-home --namespace=%s -o name" % (app_name, exec_namespace)
    cmd_output = get_command_output(cmd)
    pod_name = cmd_output.split('/')[1].split('\\')[0]
    file_path = '%s/%s:/centralized_scheduler/profiler_files_processed/profiler_home.txt' % (exec_namespace, pod_name)
    cmd = "kubectl cp " + file_path + " ."
    print("RUN: " + cmd)
    os.system(cmd)

    file_exist = False
    response_object = {"exec_profiler_info": {}}
    while not file_exist:
        try:
            f = open('profiler_home.txt')
            lines = f.readlines()
            lines.pop(0)
            json_string = json.dumps(lines)
            response_object["exec_profiler_info"] = json_string
            file_exist = True
        except FileNotFoundError:
            print("The execute information is not ready.")
            time.sleep(5)
            continue

    return jsonify(response_object), 201


def get_command_output(command):
    command = command.split(" ")
    p = subprocess.Popen(command, stdout=subprocess.PIPE)
    (output, err) = p.communicate()
    # retcode = p.wait()
    output = str(output)
    return output
