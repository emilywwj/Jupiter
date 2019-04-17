from flask import Flask, jsonify, request, render_template
from os import path
import os
from flask_cors import CORS
import json
import time

import subprocess
import sys
sys.path.append(path.abspath(__file__ + "/../../../../"))
import jupiter_config

# from demo import get_plot1, get_plot2, get_plot3, get_plot4
import demo
from bokeh.embed import server_document
from bokeh.server.server import Server
from tornado.ioloop import IOLoop
from bokeh.application import Application
from bokeh.application.handlers.function import FunctionHandler


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

    response_object = {"exec_profiler_info": {}}
    nodes = read_node_list(path.abspath(__file__ + '../../../../../') + "/nodes.txt")

    for node in nodes:
        file_exist = False
        while not file_exist:
            try:
                f = open('profiler_home.txt')
                # f = open('profiler_%s.txt'%(node))
                lines = f.readlines()
                lines.pop(0)
                json_string = json.dumps(lines)
                response_object["exec_profiler_info"]['home'] = json_string
                file_exist = True
            except FileNotFoundError:
                print("The execute information is not ready.")

                run_command_get_file('home')
                time.sleep(5)
                continue

    return jsonify(response_object), 201


def run_command_get_file(node):
    jupiter_config.set_globals()
    exec_namespace = jupiter_config.EXEC_NAMESPACE
    app_name = jupiter_config.APP_OPTION

    cmd = "kubectl get pod -l app=%s-%s --namespace=%s -o name" % (app_name, node, exec_namespace)
    cmd_output = get_command_output(cmd)
    pod_name = cmd_output.split('/')[1].split('\\')[0]
    file_path = '%s/%s:/centralized_scheduler/profiler_files_processed/profiler_%s.txt' % (exec_namespace, pod_name, node)
    cmd = "kubectl cp " + file_path + " ."
    print("RUN: " + cmd)
    os.system(cmd)


def get_command_output(command):
    command = command.split(" ")
    p = subprocess.Popen(command, stdout=subprocess.PIPE)
    (output, err) = p.communicate()
    # retcode = p.wait()
    output = str(output)
    return output


def read_node_list(path2):
    nodes = []
    node_file = open(path2, "r")
    for line in node_file:
        node_line = line.strip().split(" ")
        nodes.append(node_line[0])
    return nodes

# def get_plot():
# #     post_data = request.get_json()
# #     p = None
# #     if (post_data == 'node_info'):
#     p = get_plot2()

#     # following above points:
#     #  + pass plot object 'p' into json_item
#     #  + wrap the result in json.dumps and return to frontend
#     return json.dumps(json_item(p, "myplot"))



@app.route('/plot')
def demo_worker():
    # Can't pass num_procs > 1 in this configuration. If you need to run multiple
    # processes, see e.g. flask_gunicorn_embed.py
    apps = {'/demo': Application(FunctionHandler(modify_doc))}
    server = Server(apps, io_loop=IOLoop(), port=5006)
    server.start()
    server.io_loop.start()

def modify_doc(doc):
    demo.main(doc)


@app.route('/show_demo', methods=['GET', 'POST'])
def show_demo():
    import paho.mqtt.client as mqtt

    # The callback for when the client receives a CONNACK response from the server.
    def on_connect(client, userdata, flags, rc):
        print("Connected with result code " + str(rc))

        # Subscribing in on_connect() means that if we lose the connection and
        # reconnect then subscriptions will be renewed.
        client.subscribe("JUPITER")


    # The callback for when a PUBLISH message is received from the server.
    def on_message(client, userdata, msg):
        print(msg.topic + " " + str(msg.payload))

    client = mqtt.Client()
    client.on_connect = on_connect
    client.on_message = on_message

    client.connect("test.mosquitto.org", 1883, 60)

    # Blocking call that processes network traffic, dispatches callbacks and
    # handles reconnecting.
    # Other loop*() functions are available that give a threaded interface and a
    # manual interface.
    client.loop_forever()


# @app.route('/get_network_statistics', methods=['POST'])
# def get_network_statistics():

#     file_exist = False
#     response_object = {"network_statistics": {}}
#     while not file_exist:
#         try:
#             f = open('profiler_home.txt')
#             lines = f.readlines()
#             lines.pop(0)
#             json_string = json.dumps(lines)
#             response_object["network_statistics"] = json_string
#             file_exist = True
#         except FileNotFoundError:
#             print("The execute information is not ready.")

#             run_command_get_file()
#             time.sleep(5)
#             continue

#     return jsonify(response_object), 201

# def run_command_get_file():
#     jupiter_config.set_globals()
#     profiler_namespace = jupiter_config.PROFILER_NAMESPACE
#     app_name = jupiter_config.APP_OPTION
#     cmd = "kubectl get pod -l app=homeprofiler --namespace=%s -o name" % (profiler_namespace)
#     cmd_output = get_command_output(cmd)
#     pod_name = cmd_output.split('/')[1].split('\\')[0]
#     # file_path = '%s/%s:/network_profiling/parameters_*' % (profiler_namespace, pod_name)
    
#     cmd = "kubectl cp " + file_path + " ."
#     print("RUN: " + cmd)
#     os.system(cmd)


# def get_command_output(command):
#     command = command.split(" ")
#     p = subprocess.Popen(command, stdout=subprocess.PIPE)
#     (output, err) = p.communicate()
#     # retcode = p.wait()
#     output = str(output)
#     return output