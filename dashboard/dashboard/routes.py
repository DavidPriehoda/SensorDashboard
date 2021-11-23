from flask import render_template, url_for, redirect, request, jsonify
from flask_login import login_user, logout_user, login_required, current_user

import json

from dashboard import app
from dashboard.forms import LoginForm

sensor_data = {'01:06': '18.6', '01:26': '18.6', '01:46': '18.5', '02:06': '18.4', '02:26': '18.4', '02:46': '18.3', '03:06': '18.2', '03:26': '18.2', '03:46': '18.1', '04:06': '18.1'}

@app.route("/")
@app.route("/home")
def home():
    return render_template('home.html', sensor_data=sensor_data)


@app.route("/login",methods=["GET","POST"])
def login():
    form = LoginForm()
    
    if form.validate_on_submit():
        # user = User.query.filter_by(email=form.email.data).first()
        # if user is not None and user.verify_password(form.password.data):
        #     login_user(user)
        #     return redirect(url_for('home')) #Invalid email address or password
        # return render_template('login.html',form=form)
        return render_template("welcome.html")
    
    return render_template('login.html',title='Login',form=form)


@app.route("/graph")
def graph():
    return render_template('graph.html', sensor_data=sensor_data)


@app.route('/api/new_sensor_data/', methods = ['POST'])
def new_sensor_data():
    global sensor_data
    jsondata = request.get_json()
    data = json.loads(jsondata)
    
    sensor_data[data["DATA_ENTRY_TIME"][11:16]] = data["REPORTED_TEMP"]

    return json.dumps(True)