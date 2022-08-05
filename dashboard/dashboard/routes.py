import json
import re
from datetime import datetime, timedelta
from dateutil import parser

from flask import render_template, url_for, redirect, request, jsonify, flash, session
from flask_login import login_user, logout_user, login_required, current_user
from flask_wtf import FlaskForm, csrf
from wtforms import StringField, PasswordField, BooleanField, SubmitField
from wtforms.validators import InputRequired, Email, Length, EqualTo
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash

from dashboard import app, db, csrf
from dashboard.forms import LoginForm, RegisterForm, AccountUpdateForm, AddCarerForm, SensorLimitForm
from dashboard.models import User, Sensor, SensorEntry, UserCarer, get_user_by_api_key



@app.route("/")
@app.route("/home")
def home():
    if current_user.is_authenticated:
        return render_template('home.html', sensors=current_user.get_sensors())

    return redirect(url_for("login"))


@app.route("/register", methods=["GET", "POST"])
def register():
    UserRegister = RegisterForm()
    if request.method == 'POST':
        form = RegisterForm(request.form)
        if not form.validate():
            for field, error in form.errors.items():
                flash(f"Error - {error[0]}", 'danger')
        else:
            first_name =  request.form.get('first_name')
            last_name =  request.form.get('last_name')
            email = request.form.get('email')
            password = request.form.get('password')
            password2 = request.form.get('confirm')
            test_str = re.search(r"\W", password)
            if User.query.filter_by(Email=email).all():
                flash('Email already in use!', 'danger')
                render_template('register.html', title='Register', form=UserRegister)
            else:
                new_user = User(First_Name = first_name, Last_Name = last_name, Email = email, Password_Hash = generate_password_hash(password))
                db.session.add(new_user)
                db.session.commit()
            return render_template('login.html', form=UserRegister)
    return render_template('register.html', form=UserRegister)


@app.route("/update_user", methods=["POST"])
@login_required
def update_user():
    form = AccountUpdateForm(request.form)
    if not form.validate():
        for field, error in form.errors.items():
            flash(f"Error - {error[0]}", 'danger')
    else:
        user = db.session.query(User).get(current_user.id)
        user.First_Name =  request.form.get('first_name')
        user.Last_Name = request.form.get('last_name')
        user.Email=request.form.get('email')
        user.Is_Carer = 1 if request.form.get('is_carer') else 0
        db.session.commit()
        flash("Updated successfully!", 'success')
    user = db.session.query(User).get(current_user.id)
    return render_template("account.html", user=user)

@app.route("/login", methods=["GET", "POST"])
def login():
    UserLogin = LoginForm()
    if request.method == 'POST':
        UserLogin = LoginForm(request.form)
        if not UserLogin.validate():
            for field, error in UserLogin.errors.items():
                flash(f"Error - {error[0]}", 'danger')
        else:
            email = request.form.get('email')
            password = request.form.get('password')
            user = User.query.filter_by(Email=email).first()
            if user is not None and user.verify_password(password):
                login_user(user)
                return render_template("welcome.html", name=user.get_first_name())

            flash('Invalid Username or Password', 'danger')

    return render_template('login.html', title='Login', form=UserLogin)


@app.route("/logout")
def logout():
    logout_user()
    return redirect(url_for("login"))


@app.route("/PP")
def PP():
    return render_template('PP.html')


@app.route("/TC")
def TC():
    return render_template('T&C.html')

@app.route("/deleteaccount", methods=["POST"])
def deleteaccount():
    if current_user.is_authenticated:
        current_user.delete_user()
    return redirect(url_for("login"))


@app.route("/Account",  methods=["GET", "POST"])
def account():
    if current_user.is_authenticated:
        return render_template('Account.html', user=current_user)
    else:
        return redirect(url_for("login"))

@app.route("/carers")
def carers():
    if current_user.is_authenticated:
        f = AddCarerForm()
        return render_template('carers.html', form=f)
    return redirect(url_for("login"))

@app.route("/addcarer", methods=["POST"])
def addcarer():
    if current_user.is_authenticated:
        CarerForm = AddCarerForm(request.form)
        if not CarerForm.validate():
            for field, error in CarerForm.errors.items():
                print(error[0])
                flash(f"Error - {error[0]}", 'danger')
        else:
            carer_email = request.form.get('carer_email')
            carer = User.query.filter_by(Email=carer_email).first()
            current_carers = current_user.get_carers()

            if carer is None:
                flash("This user is not a carer.", 'danger')
                return render_template('carers.html', form=CarerForm)

            if not carer.Is_Carer:
                flash("This user is not a carer.", 'danger')
                return render_template('carers.html', form=CarerForm)

            if carer in current_carers:
                flash("You already have this user registered as a carer.")
                return render_template('carers.html', form=CarerForm)

            current_user.add_carer(carer.id)
            flash("Carer added successfully!", 'success')

        return render_template('carers.html', form=CarerForm)
    return '', 401

@app.route("/deletecarer", methods=["POST"])
def deletecarer():
    if current_user.is_authenticated:
        carer_id = request.form.get('carer_id')
        patient_id = request.form.get('patient_id')

        if current_user.id == patient_id or current_user.id == carer_id:

            carer = db.session.query(UserCarer).filter_by(User_ID=patient_id, Carer_ID=carer_id).first()

            if carer is not None:
                db.session.delete(carer)
                db.session.commit()
                return '', 200 #OK

            return '', 400 #Bad Request

    return '', 401 #Unauthorized

@app.route("/your_patients")
def your_patients():
    if current_user.is_authenticated and current_user.Is_Carer:
        return render_template('patients.html')
    return redirect(url_for("home"))


@app.route("/patient/<id>")
def patient(id):
    if current_user.is_authenticated:
        if db.session.query(UserCarer).filter_by(User_ID=id, Carer_ID=current_user.id).first():
            patient = db.session.query(User).filter_by(id=id).first()

            return render_template('patient.html',patient=patient, sensors= patient.get_sensors())
    return redirect(url_for("login"))


@app.route("/sensor/<id>")
def sensor(id):
    s = Sensor.query.filter_by(Sensor_ID = id).first()

    #Validate that the sensor belongs to the user or one of the users patients
    if s and current_user.is_authenticated and (s in current_user.get_sensors() or s.User_ID in [i.id for i in current_user.get_patients()]):
        limitform = SensorLimitForm()
        return render_template('sensor.html', sensor=s, form=limitform)

    return redirect(url_for("home"))

@app.route("/delete_sensor")
def delete_sensor():
    if current_user.is_authenticated:
        sensor_id = request.args.get('sensor_id')
        sensor = Sensor.query.filter_by(Sensor_ID = sensor_id).first()

        #Validate that the sensor belongs to the user or one of the users patients
        if sensor and (sensor in current_user.get_sensors() or sensor.User_ID in [i.id for i in current_user.get_patients()]):
            sensor.delete_sensor()
            return '', 200 #OK
    return '', 401 # Unauthorized

@app.route("/newsensor", methods=["POST"])
def newsensor():
    if current_user.is_authenticated:
        current_user.add_sensor(request.form.get('sensor_name'))
        return "", 201 # Created
    return "", 401 # Unauthorized

@app.route('/api/new_sensor_data/', methods=['POST'])
@csrf.exempt
def new_sensor_data():
    data = json.loads(request.get_json()) # [Api key, {Sensor data dictionary}]
    api_key = data[0]
    user = get_user_by_api_key(api_key)
    if user:
        sensor_data = data[1]
        users_sensors = [sensor.get_id() for sensor in user.get_sensors()] # List of sensor ids for user
        try:
            if sensor_data['SENSOR_EUI'] in users_sensors: #If sensor id belongs to user
                new_entry = SensorEntry(Sensor_ID = sensor_data.pop('SENSOR_EUI'))
                for key,value in sensor_data.items():
                    try:
                        value = float(value)
                    except ValueError:
                        if value == "null":
                            value = None
                        if key == "DATA_ENTRY_TIME":
                            #value = parser.parse(value)
                            value = datetime.now()

                    setattr(new_entry, key, value)

                db.session.add(new_entry)
                db.session.commit()
                return "", 201 # Created
        except Exception:
            pass
        return "", 400 # Bad Request
    return "", 401 # Unauthorized

@app.route("/get_sensor_data", methods=["GET"])
def get_sensor_data():
    sensor_id = request.args.get('sensor_id')
    data_type = request.args.get('data_type')
    time_option = request.args.get('time_option')

    sensor = Sensor.query.filter_by(Sensor_ID = sensor_id).first()

    data_types = {"0":"REPORTED_TEMP","1":"OUTSIDE_HUMIDITY","2":"OUTSIDE_AIRPRESSURE","3":"OUTSIDE_TEMP","4":"REPORTED_HUMIDITY","5":"LIGHT","6":"MOTION","7":"NOISE","8":"AIR_PRESSURE","9":"VOC","10":"ECO2"}

    times = {"0": timedelta(days = 1), "1": timedelta(days = 7), "2": timedelta(days = 30), "3": timedelta(days = 182), "4": timedelta(days = 365), "5": timedelta(days = 20000)}

    data = {'Sensor_ID':sensor_id} # {'Sensor_ID': 'ID', 'Summary':{'Avg': 0, 'Min': 0, 'Max': 0}, 'Data': [[timestamp, value], ...]}

    #Validate that the user is authorized to access the sensor (Sensor owner or carer of owner)
    if current_user.is_authenticated and (sensor in current_user.get_sensors() or sensor.User_ID in [i.id for i in current_user.get_patients()]):

        #data_type -1 is for getting all data from a specific sensor entry by timestamp
        if data_type == "-1":
            timestamp = request.args.get('timestamp')
            entry = SensorEntry.query.filter_by(Sensor_ID=sensor_id).filter(SensorEntry.DATA_ENTRY_TIME >= parser.parse(timestamp),
                                                                            SensorEntry.DATA_ENTRY_TIME <= parser.parse(timestamp)+timedelta(seconds=1)).first()
            if entry is not None:
                entry = vars(entry)
                entry.pop('_sa_instance_state')

                data['Data'] = entry
            else:
                data['Data'] = {}

        #Getting a specific type of data in a time range
        elif data_type in data_types and time_option in times:
            sensor_data = sensor.get_data_between(data_types[data_type], datetime.now() - times[time_option], datetime.now())

            if len(sensor_data) > 0:
                #d = list(map(lambda x: 0 if x[1] == "None" else float(x[1]), sensor_data))
                #summary = {'Avg': round(sum(d)/len(d),2), 'Min': min(d), 'Max': max(d)}
                s = sorted(sensor_data, key=lambda x: 0 if x[1] == "None" else float(x[1]))
                for d in s:
                    if d[1] == "None":
                        d[1] = 0
                avg = round(sum([float(l) for l in dict(s).values()])/len(s), 2)
                summary = {'Avg': avg, 'Min': s[0][1], 'Max': s[len(s)-1][1], 'MinDateTime':s[0][0].strftime("%b %d %Y %H:%M:%S"), 'MaxDateTime':s[1][0].strftime("%b %d %Y %H:%M:%S")}

                data['Summary'] = summary
                data['Data'] = sensor_data
            else:
                data['Summary'] = []
                data['Data'] = []


        return jsonify(data), 200
    return "",401 #Unauthorized


@app.route("/updatelimit", methods=["POST"])
def updatelimit():
    if current_user.is_authenticated:
        form = SensorLimitForm(request.form)
        if not form.validate():
            for field, error in form.errors.items():
                print(field, error[0])
                flash(f"Error - {error[0]}", 'danger')
        else:
            sensor = db.session.query(Sensor).filter_by(Sensor_ID=request.form.get("sensor_id")).first()
            if sensor:
                vals = {'in_temp_upper':request.form.get("in_temp_upper"),'in_temp_lower':request.form.get("in_temp_lower"),
                        'out_hum_upper':request.form.get("out_hum_upper"),'out_hum_lower':request.form.get("out_hum_lower"),
                        'out_airpress_upper':request.form.get("out_airpress_upper"),'out_airpress_lower':request.form.get("out_airpress_lower"),
                        'out_temp_upper':request.form.get("out_temp_upper"),'out_temp_lower':request.form.get("out_temp_lower"),
                        'in_hum_upper':request.form.get("in_hum_upper"),'in_hum_lower':request.form.get("in_hum_lower"),
                        'light_upper':request.form.get("light_upper"),'light_lower':request.form.get("light_lower"),
                        'motion_upper':request.form.get("motion_upper"),'motion_lower':request.form.get("motion_lower"),
                        'noise_upper':request.form.get("noise_upper"),'noise_lower':request.form.get("noise_lower"),
                        'in_airpress_upper':request.form.get("in_airpress_upper"),'in_airpress_lower':request.form.get("in_airpress_lower"),
                        'VOC_upper':request.form.get("VOC_upper"),'VOC_lower':request.form.get("VOC_lower"),
                        'ECO2_upper':request.form.get("ECO2_upper"),'ECO2_lower':request.form.get("ECO2_lower")}

                for key,value in vals.items():
                    sensor.set_attribute(key, int(value))

                db.session.commit()

                return "", 201
        return "Invalid entry. Please ensure all entries are whole numbers.", 400
    return "", 401


@app.route("/get_sensor_limit", methods=["GET"])
def get_sensor_limits():
    sensor_id = request.args.get('sensor_id')
    sensor = Sensor.query.filter_by(Sensor_ID = sensor_id).first()

    if current_user.is_authenticated and (sensor in current_user.get_sensors() or sensor.User_ID in [i.id for i in current_user.get_patients()]):
        limits = request.args.get('limit').split(',')
        return jsonify({'upperLimit': sensor.get_limit(limits[0]), 'lowerLimit': sensor.get_limit(limits[1])}), 200

    return "",401
