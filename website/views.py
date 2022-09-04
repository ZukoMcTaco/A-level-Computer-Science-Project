from flask import Blueprint, render_template #imports the blueprint and render template library from flask
from flask_login import login_user, login_required, logout_user, current_user #imports the libraries from flask login 

views = Blueprint('views', __name__) #creates an instance of blueprint called views and passes through name



@views.route('/')#decorator 
def home():
    'module that returns the template for the home page'
    return render_template("home.html")
@views.route('/chatbot')
@login_required #decorator which makes this page inaccessible unless the user has logged in
def chatbot_page():
    'module that returns the template for the chatbot page'
    return render_template("chatbot.html")
