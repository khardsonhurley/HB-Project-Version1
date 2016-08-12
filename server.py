
"""
Hackbright Project
Parrot: An learning tool for users seeking to learn Spanish as a second
language. 
by: Krishelle Hardson-Hurley
"""

from jinja2 import StrictUndefined

from flask import (Flask, render_template, redirect, request, flash, session)

from flask_debugtoolbar import DebugToolbarExtension

from model import connect_to_db, db, User, Article, UserArticle, Phrase, Note

import requests 
# This allows you to access the variables store in the environment on your 
# computer. 
import os 

import json 

app = Flask(__name__)

# Required to use Flask sessions and the debug toolbar
app.secret_key = "ABC"

#Google translate key for API
key = os.environ['GOOGLE_TRANSLATE_KEY']

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
        #Show the signup form to the user. 
        return render_template("signup_form.html")
        
    if request.method == "POST":
        #Process the sign up information and add user to database.
        first_name = request.form["firstname"]
        last_name = request.form["lastname"]
        email = request.form["email"]
        phone = request.form["phone"]
        username = request.form["username"]
        password = request.form["password"]
        #Change later if expanding to other language. Now just hard code. 
        language = "Spanish"
        language_level = request.form["langlevel"]

        new_user = User(email=email, username=username, password=password,
                        first_name=first_name, last_name=last_name,
                        phone=phone, language=language, 
                        language_level=language_level)
        db.session.add(new_user)
        db.session.commit()

        flash("Username: %s has been added." % username)

        return redirect("/login")

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
        username = request.form["username"]
        password = request.form["password"]

        user = User.query.filter_by(username=username).first()

        if not user:
            flash("Invalid username.")
            return redirect("/login")
        
        if user.password != password:
            flash("Incorrect password.")
            return redirect("/login")

        session["user_id"] = user.user_id

        flash("You are logged in to Parrot!")

        # return redirect("/profile/%s" % user.user_id)
        return redirect("/")


# @app.route('/profile/<int:user_id>')
# def profile():
#     """Users have a dashboard profile page that displays their name, previously
#     read articles, recommended articles."""
    
#     return render_template("dashboard.html")

@app.route('/translate')
def search_form():
    """Form to allow user to search through articles."""
    return render_template("translate.html")


# @app.route('/article/<int:article_id>')
# def article(): 
#     """Page where article will be rendered and user can start translating."""
#     pass


@app.route('/translate', methods = ["POST"])
def testing():
    """In this url is in the following format:
    https://www.googleapis.com/language/translate/v2?parameters
        parameters include: 
            key: the api key defined above
            source: the language of the article (es = Spanish)
            target: the language you want translated to (en = English)
            q: Specifies the text to translate.
    """ 
    #Getting the value in the dictionary sent by JS. 
    phrase = request.form.get("phrase")

    #Splitting the words into a list. 
    word_list = phrase.split(' ')

    #Googles url, pulling secret key into url. 
    google_url = "https://www.googleapis.com/language/translate/v2?key=%s&source=es&target=en&q=" % (key)

    #Google requires words separated by %20. 
    text = "%20".join(word_list)

    #The results I get back here is going to be JSON
    results = requests.get(google_url + text)

    #Converts the results from the http response object from json to a dictionary.
    dictresults= json.loads(results.text)

    #Gets the translated text out of the dictionary in list in dictionary.
    rawtranslation= dictresults['data']['translations'][0]['translatedText']

    #The rawtranslation uses &#39; instead of apostrophes. Replaced them.
    translation= rawtranslation.replace("&#39;","'")




    return translation











@app.route('/logout')
def logout_user():
    """Log out the user and delete user from session"""
    
    flash('You have successfully logged out.')
    del session['user_id']

    return redirect("/")



if __name__ == "__main__":
    # We have to set debug=True here, since it has to be True at the point
    # that we invoke the DebugToolbarExtension
    app.debug = True

    connect_to_db(app)

    # Use the DebugToolbar
    DebugToolbarExtension(app)

    app.run(host="0.0.0.0")
