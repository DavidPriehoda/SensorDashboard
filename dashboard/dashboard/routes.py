from flask import render_template, url_for, redirect, request, jsonify

import json

from dashboard import app

sensor_data = {'01:06': '18.6', '01:26': '18.6', '01:46': '18.5', '02:06': '18.4', '02:26': '18.4', '02:46': '18.3', '03:06': '18.2', '03:26': '18.2', '03:46': '18.1', '04:06': '18.1'}

@app.route("/")
@app.route("/home")
def home():
    return render_template('index.html', sensor_data=sensor_data)

@app.route('/api/new_sensor_data/', methods = ['POST'])
def new_sensor_data():
    global sensor_data
    jsondata = request.get_json()
    data = json.loads(jsondata)
    
    sensor_data[data["DATA_ENTRY_TIME"][11:16]] = data["REPORTED_TEMP"]

    return json.dumps(True)