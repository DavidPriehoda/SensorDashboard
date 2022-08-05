from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField, IntegerField
from wtforms.validators import InputRequired, Email, Length, EqualTo, Regexp


class LoginForm(FlaskForm):
    email = StringField('Email', validators=[InputRequired(), Email()])
    password = PasswordField('Password', validators=[InputRequired()])
    remember = BooleanField('Remember me')
    submit = SubmitField('Submit', render_kw={'class':'btn btn-primary btn-lg w-100'})


class RegisterForm(FlaskForm):
    first_name = StringField("First Name", validators=[InputRequired(), Length(max=30, message="First name cannot be longer than 30 characters.")])
    last_name = StringField("Last Name", validators=[InputRequired(), Length(max=30, message="Last name cannot be longer than 30 characters.")])
    email = StringField('Email', validators=[InputRequired(), Email()])
    password = PasswordField('Password', validators=[InputRequired(), Regexp('((?=.*[a-z])(?=.*[A-Z])(?=.*[\W]).{8,64})', message="Password must be between 8-64 characters and contain atleast 1 Uppercase letter, 1 lowercase letter and 1 special character.")])
    confirm = PasswordField('Confirm password', validators=[InputRequired(), EqualTo('password', message="Confirm Password value must be equal to password")])
    tick = BooleanField("I accept TOS", validators=[InputRequired()], render_kw={'id':'tos-check', 'class':'form-check-input'})
    submit = SubmitField('Submit', render_kw={'class':'btn btn-primary btn-lg w-100'})

class AccountUpdateForm(FlaskForm):
    first_name = StringField("First Name", validators=[InputRequired(), Length(max=30, message="First name cannot be longer than 30 characters.")])
    last_name = StringField("Last Name", validators=[InputRequired(), Length(max=30, message="Last name cannot be longer than 30 characters.")])
    email = StringField('Email', validators=[InputRequired(), Email()])
    is_carer = BooleanField('Iscarer')

class AddCarerForm(FlaskForm):
    carer_email = StringField('Email', validators=[InputRequired(), Email()], render_kw={'class':"form-control", 'placeholder':"Carer E-mail"})

class SensorLimitForm(FlaskForm):
    in_temp_lower = IntegerField('Inside temp (Low)', validators=[InputRequired()], render_kw={'class':'form-control'})
    in_temp_upper = IntegerField('Inside temp (High)', validators=[InputRequired()], render_kw={'class':'form-control'})
    out_hum_lower = IntegerField('Outside humidity (Low)', validators=[InputRequired()], render_kw={'class':'form-control'})
    out_hum_upper = IntegerField('Outside humidity (High)', validators=[InputRequired()], render_kw={'class':'form-control'})
    out_airpress_lower = IntegerField('Outside air pressure (Low)', validators=[InputRequired()], render_kw={'class':'form-control'})
    out_airpress_upper = IntegerField('Outside air pressure (High)', validators=[InputRequired()], render_kw={'class':'form-control'})
    out_temp_lower = IntegerField('Outside temp (Low)', validators=[InputRequired()], render_kw={'class':'form-control'})
    out_temp_upper = IntegerField('Outside temp (High)', validators=[InputRequired()], render_kw={'class':'form-control'})
    in_hum_lower = IntegerField('Inside humidity (Low)', validators=[InputRequired()], render_kw={'class':'form-control'})
    in_hum_upper = IntegerField('Inside humidity (High)', validators=[InputRequired()], render_kw={'class':'form-control'})
    light_lower = IntegerField('Light (Low)', validators=[InputRequired()], render_kw={'class':'form-control'})
    light_upper = IntegerField('Light (High)', validators=[InputRequired()], render_kw={'class':'form-control'})
    motion_lower = IntegerField('Motion (Low)', validators=[InputRequired()], render_kw={'class':'form-control'})
    motion_upper = IntegerField('Motion (High)', validators=[InputRequired()], render_kw={'class':'form-control'})
    noise_lower = IntegerField('Noise (Low)', validators=[InputRequired()], render_kw={'class':'form-control'})
    noise_upper = IntegerField('Noise (High)', validators=[InputRequired()], render_kw={'class':'form-control'})
    in_airpress_lower = IntegerField('Inside air pressure (Low)', validators=[InputRequired()], render_kw={'class':'form-control'})
    in_airpress_upper = IntegerField('Inside air pressure (High)', validators=[InputRequired()], render_kw={'class':'form-control'})
    VOC_lower = IntegerField('VOC (Low)', validators=[InputRequired()], render_kw={'class':'form-control'})
    VOC_upper = IntegerField('VOC (High)', validators=[InputRequired()], render_kw={'class':'form-control'})
    ECO2_lower = IntegerField('ECo2 (Low)', validators=[InputRequired()], render_kw={'class':'form-control'})
    ECO2_upper = IntegerField('ECo2 (High)', validators=[InputRequired()], render_kw={'class':'form-control'})
