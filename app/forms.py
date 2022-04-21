# Add any form classes for Flask-WTF here
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, IntegerField, SelectField, TextAreaField, EmailField
from flask_wtf.file import FileField, FileAllowed, FileRequired 
from wtforms.validators import InputRequired, Email, DataRequired


class LoginForm(FlaskForm):
    username = StringField('Username', validators=[InputRequired()])
    password = PasswordField('Password', validators=[InputRequired()])

class UserForm(FlaskForm):
    username    = StringField('Username', validators=[InputRequired()])
    password    = PasswordField('Password', validators=[InputRequired()])
    name        = StringField('Name', validators=[InputRequired()])
    email       = EmailField('email',validators=[DataRequired(),Email()])
    location    = StringField('Location', validators=[InputRequired()])
    biography   = StringField('Biography', validators=[InputRequired()])
    photo       = FileField('Photo', validators=[FileRequired(), FileAllowed(['jpg', 'png'], 'Images only!') ])

class CarForm(FlaskForm):
    description    = TextAreaField('description', validators=[InputRequired()])
    make           = StringField('Make', validators=[InputRequired()])
    model          = StringField('Model', validators=[InputRequired()])
    colour         = StringField('Colour', validators=[InputRequired()])
    year           = IntegerField('Year', validators=[InputRequired()])
    transmission   = StringField('Transmission', validators=[InputRequired()])
    car_type       = StringField('Type', validators=[InputRequired()])
    price          = IntegerField('Price', validators=[InputRequired()])
    photo          = FileField('Photo', validators=[FileRequired(), FileAllowed(['jpg', 'png'], 'Images only!') ])