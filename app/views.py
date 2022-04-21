"""
Flask Documentation:     https://flask.palletsprojects.com/
Jinja2 Documentation:    https://jinja.palletsprojects.com/
Werkzeug Documentation:  https://werkzeug.palletsprojects.com/
This file creates your application.
"""


  
from app import app, db, login_manager
from flask import render_template, request, redirect, url_for, flash, jsonify, send_file, _request_ctx_stack, g, make_response, send_from_directory
from flask_login import login_user, logout_user, current_user, login_required
from app.forms import LoginForm, CarForm, UserForm
from app.models import UserProfile, Car, Favourites
from werkzeug.security import check_password_hash
from werkzeug.utils import secure_filename
from flask_wtf.csrf import generate_csrf
from os import getcwd, listdir
from os.path import join
from datetime import datetime, timezone, timedelta
from time import time
# Using JWT
import jwt 
from functools import wraps

# TIMEZONE SETTINGS
jm = timezone(timedelta(hours=-5))


###
# Routing for your application.
###


@app.route('/')
def index():
    return jsonify(message="This is the beginning of our API")


# Create a JWT @requires_auth decorator
# This decorator can be used to denote that a specific route should check
# for a valid JWT token before displaying the contents of that route.
def requires_auth(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        auth = request.headers.get('Authorization', None) # or request.cookies.get('token', None) 

        if not auth:
            return jsonify({'code': 'authorization_header_missing', 'description': 'Authorization header is expected'}), 401

        parts = auth.split()

        if parts[0].lower() != 'bearer':
            return jsonify({'code': 'invalid_header', 'description': 'Authorization header must start with Bearer'}), 401
        elif len(parts) == 1:
            return jsonify({'code': 'invalid_header', 'description': 'Token not found'}), 401
        elif len(parts) > 2:
            return jsonify({'code': 'invalid_header', 'description': 'Authorization header must be Bearer + \s + token'}), 401

        token = parts[1]
        try:
            payload = jwt.decode(token, app.config['SECRET_KEY'], algorithms=["HS256"])

        except jwt.ExpiredSignatureError:
            return jsonify({'code': 'token_expired', 'description': 'token is expired'}), 401
        except jwt.DecodeError:
            return jsonify({'code': 'token_invalid_signature', 'description': 'Token signature is invalid'}), 401

        g.current_user = user = payload
        return f(*args, **kwargs)

    return decorated


@app.route('/api/csrf-token', methods=['GET'])
def get_csrf():
    return jsonify({'csrf_token': generate_csrf()})

@app.route('/api/jwt-token', methods=['GET'])
@requires_auth
def check_jwt_token():
    return jsonify({'message': "User already logged in"})


@app.route('/api/register',methods=['POST'])
#@requires_auth
def register():

    if request.method == 'POST':
        form = UserForm()
        if form.validate_on_submit():
            # process form data
            username        = form.username.data
            password        = form.password.data
            name            = form.name.data
            email           = form.email.data
            location        = form.location.data 
            biography       = form.biography.data 
            photo           = form.photo.data
            filename        = secure_filename(photo.filename)
            photo.save( join( getcwd(),app.config['UPLOAD_FOLDER'] , filename))
            dateoftimestamp 	= datetime.fromtimestamp(time())
            date    			= dateoftimestamp.astimezone(jm).strftime('%Y-%m-%d %H:%M:%S')

            print(f"USERNAME {username}  EMAIL {email}")
            #user = UserProfile.query.filter_by(username=username,email=email).first()
            usernamefound = UserProfile.query.filter_by(username=username).first()
            emailfound    = UserProfile.query.filter_by(email=email).first()



            if usernamefound is not None  :  

                message = {"message":"user already exist","status":"Username Taken"}
                return jsonify(message)

            elif  emailfound is not None :  
                              
                message = {"message":"user already exist","status":"Account Already Exist"}
                return jsonify(message)

            else:
                # Insert to database
                newuser = UserProfile(username,password,name,email,location,biography,filename,date)
                db.session.add(newuser)
                db.session.commit()
                message = {"message":"New user profile created"}
                return jsonify(message)
            
        else:
            errors = form_errors(form)
            return jsonify({"message":"Form errors","errors": errors})




@app.route("/api/auth/login", methods=["POST"])
def login():
    form = LoginForm() 

    if request.method == "POST":
        # change this to actually validate the entire form submission
        # and not just one field
        if form.validate_on_submit():
            # Get the username and password values from the form.
            username = form.username.data
            password = form.password.data

            # using your model, query database for a user based on the username
            # and password submitted. Remember you need to compare the password hash.
            # You will need to import the appropriate function to do so.
            # Then store the result of that query to a `user` variable so it can be
            # passed to the login_user() method below.
            user = UserProfile.query.filter_by(username=username).first()


            if user is not None and check_password_hash(user.password, password):
                remember_me = False

                # get user id, load into session
                login_user(user)
                payload = {
                            'sub': user.id, # subject, usually a unique identifier
                            'name': user.username,
                            'iat':  datetime.now(timezone.utc), # issued at time
                            'exp':  datetime.now(timezone.utc) + timedelta(minutes=20) # expiration time
                        }
                token = jwt.encode(payload, app.config['SECRET_KEY'], algorithm='HS256')
                message = {"message":"Login successfully","token":token, "user":user.username,"user_id":user.id}
                return jsonify(message)


            else: 
                message = {"message":"User does not exist"}
                return jsonify(message)
            
        else :
            errors = form_errors(form)
            return jsonify({"message":"Form errors","errors": errors})


# user_loader callback. This callback is used to reload the user object from
# the user ID stored in the session
@login_manager.user_loader
def load_user(id):
    return UserProfile.query.get(int(id))


@app.route("/api/auth/logout")
def logout():
    logout_user()
    #flash('Logged out successfully.', 'danger')
    #return redirect(url_for("home"))
    message = {"message":"Logged out successfully"}
    return jsonify(message)


@app.route('/api/cars', methods=['GET','POST'])
@requires_auth
def managecars():
     
    if request.method == 'GET': 
        # Return all cars stored in database
        found = Car.query.all()
        data = [Car.convert(x) for x in found] 
        
        message = {"results":data}
        return message  
    
     
    if request.method == 'POST':
        # Add a new car to the database
        form = CarForm()

        if form.validate_on_submit():
            # process form data
            description     = form.description.data
            make            = form.make.data
            model           = form.model.data
            colour          = form.colour.data
            year            = form.year.data
            transmission    = form.transmission.data
            car_type        = form.car_type.data
            price           = form.price.data     
            photo           = form.photo.data
            filename        = secure_filename(photo.filename)
             
            photo.save( join( getcwd(),app.config['UPLOAD_FOLDER'] , filename)) 

            # Check if car is already in database
            user = Car.query.filter_by(make=make,model=model,year=str(year),colour=colour,photo=filename).first()
                


            if user is not None  :                
                message = {"message":"user already exist"}
                return jsonify(message)

            else:
                # Insert to database
                newcar = Car(description, make, model, colour,year, transmission,car_type, price, filename,current_user.id)
                db.session.add(newcar)
                db.session.commit()
                message = {"message":"New car added","car":f'{year} {make} {model} added'}
                return jsonify(message)
            
        else:
            errors = form_errors(form)
            return jsonify({"message":"Form errors","errors": errors}) 



@app.route('/api/users/<user_id>', methods=['GET'])
def get_user(user_id):
    if request.method == 'GET':
        user = UserProfile.query.filter_by(id=user_id).first()  
        if user  is not None :
            data   = UserProfile.convert(user) 
            message = {"success": data}
            return  jsonify(message)
        else:
            message = {"message":"User does not exist"}
            return jsonify(message)



@app.route('/api/users/<user_id>/favouriteid', methods=['GET'])
def get_user_favourite_id(user_id):
    if request.method == 'GET':
        fav = Favourites.query.filter_by(user_id=user_id).all()  
        if fav  is not None :    
            data   = [Favourites.convert(x) for x in fav]
            message = {"favourites": data}
            return message
        else:
            message = {"message":"No favourites for this user"}
            return jsonify(message)



@app.route('/api/users/<user_id>/favourites', methods=['GET'])
def get_user_favourites(user_id):
    if request.method == 'GET':
        fav = Favourites.query.filter_by(user_id=user_id).all()  
        
        if fav  is not None :    
            data   = [Favourites.convert(x) for x in fav]
            result = [Car.convert(Car.query.filter_by(id=favourite["car_id"]).first()) for favourite in data ]
            message = {"favourites": result}
            return message
        else:
            message = {"message":"No favourites for this user"}
            return jsonify(message)



@app.route('/api/cars/<car_id>', methods=['GET'])
def get_car(car_id):
    if request.method == 'GET':
        car = Car.query.filter_by(id=car_id).first()  
        if car  is not None :
            data   = Car.convert(car) 
            message = {"success": data}
            return  jsonify(message)
        else:
            message = {"message":"Car does not exist car"}
            return jsonify(message)



@app.route('/api/cars/<car_id>/favourite', methods=['POST'])
def get_favourites(car_id):
    if request.method == 'POST':
        user_id = request.json["user_id"] 

        # check if use exist before adding a favorite car
        user = UserProfile.query.filter_by(id=user_id).first()  
        if user  is not None :
            favourite = Favourites(car_id=car_id,user_id=user_id) 
            db.session.add(favourite)
            db.session.commit()  
            message = {"success":f"Favourite add for {user.username} "}
            return jsonify(message)

        else:            
            message = {"message":"Cannot add Favourite to a none existing user"}
            return jsonify(message)
    else:            
            message = {"message":"Favourite request failed"}
            return jsonify(message)
    

@app.route('/api/cars/<car_id>/favourite/delete', methods=['POST'])
def delete_favourites(car_id):
    if request.method == 'POST':
        user_id = request.json["user_id"]        

        # check if use exist before adding a favorite car
        user = UserProfile.query.filter_by(id=user_id).first()  
        if user  is not None :
            favourite = Favourites.query.filter_by(car_id=car_id,user_id=user_id).first()
            db.session.delete(favourite)
            db.session.commit()  
            message = {"success":f"Favourite deleted for {user.username} "}
            return jsonify(message)

        else:            
            message = {"message":"Cannot delete Favourite to a none existing user"}
            return jsonify(message)
    else:            
            message = {"message":"Favourite delete request failed"}
            return jsonify(message)


@app.route('/api/search', methods=['GET'])
def searchbymake():
    if request.method == 'GET':
        make  = request.args.get("make").capitalize()
        model = request.args.get("model").capitalize()

        if make == "" and len(model) > 0:
            found   = Car.query.filter_by(model=model).all() 
        elif model == "" and len(make) > 0:
            found   = Car.query.filter_by(make=make ).all()  
        else:
            found   = Car.query.filter_by(make=make,model=model).all()  

        
        if found  is not None :    
            data   = [Car.convert(x) for x in found]
            message = {"results": data}
            return message
        else:
            message = {"message":"No cars exist for that make or model"}
            return jsonify(message)

        

@app.route('/api/users/delete', methods=['POST'])
def delete_account():
    # DELETE A USER ACCOUNT
    if request.method == 'POST':
        user_id = request.json["user_id"]        

        # check if use exist before adding a favorite car
        user = UserProfile.query.filter_by(id=user_id).first()          

        if user  is not None :
            """
            user = UserProfile.query.filter_by(id=user_id).delete()
            cars = Car.query.filter_by(user_id=user_id).delete()
            favourite = Favourites.query.filter_by(user_id=user_id).delete()
            """
            user = db.session.query(UserProfile).filter(UserProfile.id==user_id).delete()
            cars = db.session.query(Car).filter(Car.user_id==user_id).delete()
            favourite = db.session.query(Favourites).filter(Favourites.user_id==user_id).delete()
            db.session.commit()
            print(f"RESULTS IN DELETE REQUEST  USER {user}  CARS {cars} FAVS {favourite}")

            # LOG USER 
            logout_user()
            
            message = {"success":f"Account deleted for {user_id} "}
            return jsonify(message)

        else:            
            message = {"message":"Cannot delete account to a none existing user"}
            return jsonify(message)
    else:            
            message = {"message":"Favourite delete request failed"}
            return jsonify(message)


@app.route('/api/images/<image_id>')
#@login_required
def get_images(image_id):   
    return send_from_directory( join( getcwd(),app.config['UPLOAD_FOLDER']),image_id )


def get_uploaded_images(rootdir,uploaddir):
    images = []
    try:
        images = listdir(join(rootdir,uploaddir))
    except Exception as e:
        print(e)
    else:
        print("complete")

    return images



###
# The functions below should be applicable to all Flask apps.
###

# Here we define a function to collect form errors from Flask-WTF
# which we can later use
def form_errors(form):
    error_messages = []
    """Collects form errors"""
    for field, errors in form.errors.items():
        for error in errors:
            message = u"Error in the %s field - %s" % (
                    getattr(form, field).label.text,
                    error
                )
            error_messages.append(message)

    return error_messages


@app.route('/<file_name>.txt')
def send_text_file(file_name):
    """Send your static text file."""
    file_dot_text = file_name + '.txt'
    return app.send_static_file(file_dot_text)


@app.after_request
def add_header(response):
    """
    Add headers to both force latest IE rendering engine or Chrome Frame,
    and also tell the browser not to cache the rendered page. If we wanted
    to we could change max-age to 600 seconds which would be 10 minutes.
    """
    response.headers['X-UA-Compatible'] = 'IE=Edge,chrome=1'
    response.headers['Cache-Control'] = 'public, max-age=0'
    return response


@app.errorhandler(404)
def page_not_found(error):
    """Custom 404 page."""
    return jsonify(error="Page Not Found"), 404


if __name__ == '__main__':
    app.run(debug=True,host="0.0.0.0",port="8080")