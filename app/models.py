# Add any model classes for Flask-SQLAlchemy here
from flask import jsonify
from . import db
from werkzeug.security import generate_password_hash
from secrets import token_hex
from json import loads, dumps

class UserProfile(db.Model):
    # You can use this to change the table name. The default convention is to use
    # the class name. In this case a class name of UserProfile would create a
    # user_profile (singular) table, but if we specify __tablename__ we can change it
    # to `user_profiles` (plural) or some other name.
    __tablename__ = 'user_profiles'

    id             = db.Column(db.Integer, primary_key=True)
    username       = db.Column(db.String(80), unique=True)
    password       = db.Column(db.String(255))
    name           = db.Column(db.String(80))
    email          = db.Column(db.String(80), unique=True)
    location       = db.Column(db.String(80))
    biography      = db.Column(db.String(1000))
    photo          = db.Column(db.String(80))
    date_join      = db.Column(db.DateTime(80))
    
    

    def __init__(self, username, password, name, email, location, biography, photo, date):
        self.username   = username 
        self.password   = generate_password_hash(password, method='pbkdf2:sha256')        
        self.name       = name        
        self.email      = email
        self.location   = location
        self.biography  = biography
        self.photo      = photo
        self.date_join  = date


    def convert(user):
        userprofile = {
            "id"                : user.id,
            "username"          : user.username,
            "name"              : user.name,
            "email"             : user.email,
            "location"          : user.location,
            "biography"         : user.biography,
            "photo"             : user.photo,
            "date_join"         : user.date_join,
                }
        return userprofile

    def is_authenticated(self):
        return True

    def is_active(self):
        return True

    def is_anonymous(self):
        return False

    def get_id(self):
        try:
            return unicode(self.id)  # python 2 support
        except NameError:
            return str(self.id)  # python 3 support

    def __repr__(self):
        return '<User %r>' % (self.id)



class Car(db.Model):
    # You can use this to change the table name. The default convention is to use
    # the class name. In this case a class name of UserProfile would create a
    # user_profile (singular) table, but if we specify __tablename__ we can change it
    # to `user_profiles` (plural) or some other name.
    __tablename__ = 'car'

    id              = db.Column(db.Integer, primary_key=True  , autoincrement=True)
    description     = db.Column(db.String(1000))
    make            = db.Column(db.String(80))
    model           = db.Column(db.String(80))
    colour          = db.Column(db.String(80))
    year            = db.Column(db.String(80))
    transmission    = db.Column(db.String(80))
    car_type        = db.Column(db.String(80))
    price           = db.Column(db.Float)
    photo           = db.Column(db.String(80))
    user_id         = db.Column(db.Integer) 

    def __init__(self, description, make, model, colour,year, transmission,car_type, price, photo, user_id):
        self.description    = description
        self.make           = make
        self.model          = model
        self.colour         = colour
        self.year           = year
        self.transmission   = transmission
        self.car_type       = car_type
        self.price          = price
        self.photo          = photo 
        self.user_id        = user_id  #token_hex(15)


    def convert(Car):
        car = {
            "id"                : Car.id,
            "description"       : Car.description,
            "make"              : Car.make,
            "model"             : Car.model,
            "colour"            : Car.colour,
            "year"              : Car.year,
            "transmission"      : Car.transmission,
            "car_type"          : Car.car_type,
            "price"             : Car.price,
            "photo"             : Car.photo,
            "user_id"           : Car.user_id
                }
        return car

    def is_authenticated(self):
        return True

    def is_active(self):
        return True

    def is_anonymous(self):
        return False

    def get_id(self):
        try:
            return unicode(self.id)  # python 2 support
        except NameError:
            return str(self.id)  # python 3 support

    def __repr__(self):
        
        return    '<User %r>' % (self.id)


class Favourites(db.Model):
    # You can use this to change the table name. The default convention is to use
    # the class name. In this case a class name of UserProfile would create a
    # user_profile (singular) table, but if we specify __tablename__ we can change it
    # to `user_profiles` (plural) or some other name.
    __tablename__ = 'favourites'

    id              = db.Column(db.Integer, primary_key=True  , autoincrement=True) 
    car_id          = db.Column(db.Integer) 
    user_id         = db.Column(db.Integer) 

    def __init__(self, car_id, user_id): 
        self.car_id         = car_id
        self.user_id        = user_id


    def convert(Fav):
        Fav = { "car_id" : Fav.car_id }
        return Fav

    def is_authenticated(self):
        return True

    def is_active(self):
        return True

    def is_anonymous(self):
        return False

    def get_id(self):
        try:
            return unicode(self.id)  # python 2 support
        except NameError:
            return str(self.id)  # python 3 support

    def __repr__(self):
        return '<User %r>' % (self.user_id)