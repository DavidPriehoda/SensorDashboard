from uuid import uuid4
from secrets import token_urlsafe
from datetime import datetime, timedelta
from dateutil import parser

from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin

from dashboard import db, login_manager


class User(db.Model,UserMixin):
    id = db.Column(db.String(36), default=str(uuid4()), primary_key=True)
    First_Name = db.Column(db.String(24),nullable=False)
    Last_Name = db.Column(db.String(24),nullable=False)
    Email = db.Column(db.String(64), nullable=False, unique=True)
    Password_Hash = db.Column(db.String(96), nullable=False)
    Is_Carer = db.Column(db.Boolean(), default=False)
    API_Key = db.Column(db.String(32), default = token_urlsafe(24))

    def __repr__(self):
        return f"User(ID: {self.id})"

    def verify_password(self,password):
        return check_password_hash(self.Password_Hash,password)

    def get_first_name(self):
        return self.First_Name

    def get_last_name(self):
        return self.Last_Name

    def get_email(self):
        return self.Email

    def get_initials(self):
        return self.First_Name[0] + self.Last_Name[0]

    def add_sensor(self,sensor_name):
        new_sensor = Sensor(Sensor_ID=str(uuid4()),User_ID=self.id, Sensor_Name=sensor_name)
        db.session.add(new_sensor)
        db.session.commit()
        return new_sensor

    def get_sensors(self):
        return Sensor.query.filter_by(User_ID=self.id).all()

    def gen_new_api_key(self):
        self.API_Key = token_urlsafe(24)
        db.session.commit()
        return self.API_Key

    def get_api_key(self):
        return self.API_Key

    def add_carer(self, carer_id):
        new_carer = UserCarer(User_ID=self.id, Carer_ID=carer_id)
        db.session.add(new_carer)
        db.session.commit()
        return new_carer


    def get_carers(self):
        carer_ids = UserCarer.query.filter_by(User_ID=self.id).all()
        carers = []
        for carer in carer_ids:
            carers.append(User.query.filter_by(id=carer.Carer_ID).first())

        return carers

    def get_patients(self):
        patient_ids = UserCarer.query.filter_by(Carer_ID=self.id).all()
        patients = []
        for patient in patient_ids:
            patients.append(User.query.filter_by(id=patient.User_ID).first())

        return patients

    def delete_user(self):
        #Delete all of users sensors
        for sensor in self.get_sensors():
            sensor.delete_sensor()

        db.session.delete(self)
        db.session.commit()
        return True

def get_user_by_api_key(api_key):
    return User.query.filter_by(API_Key=api_key).first()

@login_manager.user_loader
def load_user(id):
    return User.query.get(id)

class UserCarer(db.Model):
    Carer_ID = db.Column(db.String(36), primary_key=True)
    User_ID = db.Column(db.String(36), primary_key=True)
    Carer_Since = db.Column(db.DateTime(), default=db.func.now())


class SensorEntry(db.Model):
    Sensor_ID =  db.Column(db.String(36), nullable = False, primary_key=True)
    DATA_ENTRY_TIME = db.Column(db.DateTime(), default=db.func.now(), primary_key=True)
    OUTSIDE_TEMP = db.Column(db.Float(), default = None)
    OUTSIDE_HUMIDITY = db.Column(db.Float(), default = None)
    OUTSIDE_AIRPRESSURE = db.Column(db.Float(), default = None)
    IDENTIFIER_DESCRIPTION = db.Column(db.String(32), default = None)
    REPORTED_TEMP = db.Column(db.Float(), default = None)
    REPORTED_HUMIDITY = db.Column(db.Float(), default = None)
    LIGHT = db.Column(db.Float(), default = None)
    MOTION = db.Column(db.Float(), default = None)
    NOISE = db.Column(db.Float(), default = None)
    AIR_PRESSURE = db.Column(db.Float(), default = None)
    VOC = db.Column(db.Float(), default = None)
    ECO2 = db.Column(db.Float(), default = None)

    def __repr__(self):
        return f"Sensor Entry(ID: {self.Sensor_ID} Time: {self.DATA_ENTRY_TIME})"


class Sensor(db.Model):
    Sensor_ID =  db.Column(db.String(36), default=str(uuid4()), primary_key=True)
    User_ID = db.Column(db.String(36), nullable=False)
    Sensor_Name = db.Column(db.String(32), default="Sensor")
    #Limits
    in_temp_upper = db.Column(db.Integer, default=27, nullable=False)
    in_temp_lower = db.Column(db.Integer, default=0, nullable=False)
    out_hum_upper = db.Column(db.Integer, default=50, nullable=False)
    out_hum_lower = db.Column(db.Integer, default=30, nullable=False)
    out_airpress_upper = db.Column(db.Integer, default=1050, nullable=False)
    out_airpress_lower = db.Column(db.Integer, default=950, nullable=False)
    out_temp_upper = db.Column(db.Integer, default=27, nullable=False)
    out_temp_lower = db.Column(db.Integer, default=0, nullable=False)
    in_hum_upper = db.Column(db.Integer, default=50, nullable=False)
    in_hum_lower = db.Column(db.Integer, default=30, nullable=False)
    light_upper = db.Column(db.Integer, default=300, nullable=False)
    light_lower = db.Column(db.Integer, default=0, nullable=False)
    motion_upper = db.Column(db.Integer, default=70, nullable=False)
    motion_lower = db.Column(db.Integer, default=0, nullable=False)
    noise_upper = db.Column(db.Integer, default=85, nullable=False)
    noise_lower = db.Column(db.Integer, default=0, nullable=False)
    in_airpress_upper = db.Column(db.Integer, default=1050, nullable=False)
    in_airpress_lower = db.Column(db.Integer, default=950, nullable=False)
    VOC_upper = db.Column(db.Integer, default=3000, nullable=False)
    VOC_lower = db.Column(db.Integer, default=0, nullable=False)
    ECO2_upper = db.Column(db.Integer, default=2000, nullable=False)
    ECO2_lower = db.Column(db.Integer, default=0, nullable=False)

    def get_id(self):
        return self.Sensor_ID

    def get_name(self):
        return self.Sensor_Name

    def get_entries_between(self, start_time, end_time=datetime.now()):
        #Return all sensors entries from a given time period
        return SensorEntry.query.filter_by(Sensor_ID=self.Sensor_ID).filter(SensorEntry.DATA_ENTRY_TIME >= start_time, SensorEntry.DATA_ENTRY_TIME <= end_time).all()

    def get_data_between(self, data_type, start_time, end_time=datetime.now):
        entries = self.get_entries_between(start_time, end_time)
        data = []

        if len(entries) > 0 and hasattr(entries[0], data_type):
            for entry in entries:
                data.append([entry.DATA_ENTRY_TIME, str(getattr(entry,data_type))])

        return data

    def get_limit(self, id):
        return getattr(self, id)

    def delete_sensor(self):
        db.session.query(SensorEntry).filter_by(Sensor_ID=self.Sensor_ID).delete()
        db.session.delete(self)
        db.session.commit()
        return True
    
    def set_attribute(self, name, value):
        setattr(self, name, value)
        return True

    def __repr__(self):
        return f"Sensor(ID: {self.Sensor_ID})"
