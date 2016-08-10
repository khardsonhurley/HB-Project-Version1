
"""
Hackbright Project
Parrot: An learning tool for users seeking to learn Spanish as a second
language. 
by: Krishelle Hardson-Hurley
"""

from jinja2 import StrictUndefined

from flask import (Flask, render_template, redirect, request, flash, session)

from flask_debugtoolbar import DebugToolbarExtension

from model import connect_to_db, db


app = Flask(__name__)

# Required to use Flask sessions and the debug toolbar
app.secret_key = "ABC"

# Normally, if you use an undefined variable in Jinja2, it fails silently.
# This is horrible. Fix this so that, instead, it raises an error.
app.jinja_env.undefined = StrictUndefined


@app.route('/')
def index():
    """Homepage with description and BEGIN button."""

    return render_template("home.html")

@app.route('/startpage')
def startpage():
    """Start page where user can chose log in or sign up."""

    return render_template("start_page.html")

@app.route('/signup', methods=["GET", "POST"])
def signup_process(): 
    """Users sign up for an account."""
    
    if request.method == "GET":
        return render_template("signup_form.html")
    
    if request.method == "POST":
        pass
    pass

# Not sure if this will just be part of the profile or the signup process. 
# @app.route('/preferences')
# def preferences():
#     """After user initiates sign up process, they enter their preferences 
#     (topics they are interested in)."""
#     pass

@app.route('/login', methods=["GET", "POST"])
def login():
    """Users who already have an account can log in"""
    if request.method == "GET":
        return render_template("login_form.html")
    
    if request.method == "POST":
        pass
    pass


@app.route('/profile/<int:user_id>')
def profile():
    """Users have a dashboard profile page that displays their name, previously
    read articles, recommended articles."""
    pass

@app.route('/search')
def search_form():
    """Form to allow user to search through articles."""
    pass


@app.route('/article/<int:article_id>')
def article(): 
    """Page where article will be rendered and user can start translating."""
    pass

@app.route('/logout')
def logout_user():
    """Log out the user and delete user from session"""
    
    flash('You have successfully logged out.')
    del session['user']

    return redirect("/")



if __name__ == "__main__":
    # We have to set debug=True here, since it has to be True at the point
    # that we invoke the DebugToolbarExtension
    app.debug = True

    connect_to_db(app)

    # Use the DebugToolbar
    DebugToolbarExtension(app)

    app.run(host="0.0.0.0")
