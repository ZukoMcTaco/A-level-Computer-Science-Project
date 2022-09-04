from flask import Blueprint, jsonify, render_template, request, flash, redirect, url_for, session
from .models import User
from werkzeug.security import generate_password_hash, check_password_hash
from . import db
from flask_login import login_user, login_required, logout_user, current_user
from .chat import get_response



auth =Blueprint('auth', __name__)

@auth.route("/login", methods=['GET','POST'])
def login():
    'function that renders the template for the log in page'
    if request.method =='POST':
        username = request.form.get('username')#gets username inputted by user
        password = request.form.get('password')#gets password inputted by user
        user = User.query.filter_by(username=username).first()#queries if user is in db
        if user:
            if check_password_hash(user.password, password):
                flash('Log in successful :)', category='success')#user logged in successfully
                login_user(user, remember=True)#logs user in and remembers that they've logged in
                session['logged_in']=True#session variable set to True to display correct navbar
                return redirect(url_for('views.home'))#redirects user to the home page

            else:
                flash('Incorrect password please try again ', category='error')
                #displays error message as user inputted the wrong password
        else:
            flash('Username does not exist, please try again', category='error')
            #error message displayed to notify user that their username isn't in the db

    return render_template("login.html", user=current_user)#renders the template for the login page

@auth.route("/logout")
@login_required
def logout():
    'function that renders the template for the log out page'
    session['logged_in']=False#session variable set to false to change navbar back to the version seen
    #by user that aren't logged in
    flash('Logged out successfully :)', category='success')
    #flashes message that user has logged out
    logout_user()#logs user out function from flask
    return redirect(url_for('auth.login'))#redirects user to login page

@auth.route("/sign-up",methods=['GET','POST'])
def sign_up():
    'function that renders the template for the sign up page'
    if request.method =='POST':
        email =request.form.get('email')#gets user's email
        username =request.form.get('username')#gets user's usernam
        password1 = request.form.get('password')#gets user password
        password2 = request.form.get('password2')#gets their second inputted password for valdiation
        user = User.query.filter_by(username=username).first()#queries if username is already in db
        email_exists=User.query.filter_by(email=email).first()#queries if email is already in db
        if user:
            flash('Username already exists', category='error')# if the username is already taken this message will be displayed
        elif email_exists:
            flash('Email already exists', category='error')# if the email is already taken this message will be displayed
        elif len(username)==0:
            #If username field is empty it will display error message
            flash("Enter your username", category='error')
        elif len(email)==0:
            #If email field is empty it will display error message
            flash("Enter an email address", category='error')
        elif len(password1)==0:
            #If password field is empty it will display error message
            flash("Enter a password", category='error')
        elif len(username)<5:
            #If username field is less than 5 characters it will display error message
            flash("Username is less than 5 characters", category='error')
        elif not(any(x.isupper() for x in password1)):
            flash("The password entered does not have a Capital letter", category='error')
            #If password doeos not contain a capital letter it will display 
        elif not(any(x.isdigit() for x in password1)):
            #if password doesn't contain a capital letter it will display error message
            flash("The password entered must contain a number", category='error')
        elif 8>len(password1) or len(password1)>15:
            #If password not between 8 and 15 characters it will display error message
            flash("The password entered must be between 8 to 15 characters", category='error')
        elif password1 != password2:
            #if password doesn't match then it will display the error message
            flash('The password entered does not match >:(', category='error')
      
        else:
            new_user= User(email=email , username=username, password=generate_password_hash(password1, method='sha256'))
            #creates an instance of the User and also hashes the password created
            db.session.add(new_user) #stores the user data into the database
            db.session.commit()#commits the sql
            session['logged_in']=True #sets a session variable: used to display correct navbar
            flash('Account successfully created', category='success')#success message displayed
            login_user(new_user, remember=True)#logs user in and remembers they've logged in
            return redirect(url_for('views.home'))#redirects user to the home page

    return render_template("sign_up.html", user=current_user)#renders the sign up page
@auth.route("/reset", methods=['GET','POST'])
def reset():
    'function that renders the reset password page'
    email =request.form.get('email')#email is taken from user input
    password1= request.form.get('password')#password is taken from user input
    password2= request.form.get('password2')#the user is forced to enter their password again
    email_exists=User.query.filter_by(email=email).first()#queries if email is in database
    if not email_exists:
        flash('The email you entered does not have a registered account', category='error')
    elif 8>len(password1) or len(password1)>15:
        #If password not between 8 and 15 characters it will display error message
        flash("The password entered must be between 8 to 15 characters", category='error')
    elif not(any(x.isupper() for x in password1)):
        flash("The password entered does not have a Capital letter", category='error')
    elif not(any(x.isdigit() for x in password1)):
        #if password doesn't contain a capital letter it will display error message
        flash("The password entered must contain a number", category='error')
    elif 8>len(password1) or len(password1)>15:
        #If password not between 8 and 15 characters it will display error message
        flash("The password entered must be between 8 to 15 characters", category='error')
    elif password1 != password2:
        #error message flashed if passwords do not match
        flash('The password you entered did not match', category="error")
    else:
        #if password is valid it will be updated on the database
        email_exists.password=generate_password_hash(password1, method='sha256')
        db.session.commit()
        flash('Password change successful', category="success")
    return render_template("reset.html")#renders the reset password page

@auth.route('/chatbot')
@login_required #decorator which makes this page inaccessible unless the user has logged in
def chatbot_page():
    'module that returns the template for the chatbot page'
    return render_template("chatbot.html")

@auth.post("/predict")
def predict():
    "route function that communicates with the javascript which controls the displaying of the text on screen"
    text= request.get_json("message")["message"]#gets the user's message
    bot_contents= get_response(text)#gets the bot contents from the module get_response
    response=bot_contents[0]#contains the chatbot's response
    bot_mood=bot_contents[1]#contain's the bot's mood
    message={"answer": response,"bot_mood":bot_mood}#creates a dictionary which contains the response and mood of bot
    return jsonify(message)#jsonifies and returns the message to the javascript