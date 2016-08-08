"""Models and database functions for Parrot"""


#allows me to use the session object
from flask_sqlalchemy import SQLAlchemy 

db = SQLAlchemy()

################################################################################
#Model definitions

class User(db.Model):
    """User of Parrot website"""

    __tablename__ = "users"

    user_id = db.Column(db.Integer, 
                        autoincrement=True,
                        primary_key=True)
    email = db.Column(db.String(50), nullable=True)
    username = db.Column(db.String(50), nullable=False)
    first_name = db.Column(db.String(50),nullable=True)
    last_name = db.Column(db.String(50),nullable=True)
    """
    ******************QUESTION*******************
    What do I do about the type for phone? Will use Twilio API, need to define
    so it is compatible.
    """
    phone = db.Column(db.String(10), nullable=True)
    #Here will auto seed Spanish until enable other language features. 
    language = db.Column(db.String(15),nullable=True)
    #Consult language proficiency resource
    language_level = db.Column(db.String(15),nullable=True)

    article = db.relationship('Article', backref= 'user')

class Article(db.Model):
    """Articles available to users."""

    __tablename__ = "articles"

    article_id = db.Column(db.Integer, 
                        autoincrement=True,
                        primary_key=True)
    title = db.Column(db.String(100), nullable=True)
    author= db.Column(db.String(50), nullable=True)
    """
    ******************QUESTION*******************
    Do I need to have an association table and do a lang_id? For now all Spanish.
    But what if later I add more? What do I do? 
    """
    language = db.Column(db.String(15), nullable=True)
    url = db.Column(db.String(100), nullable=True)
    text = db.Column(db.Text, nullable=False)

class UserArticle(db.Model):
    """Association table between users and articles. Shows which articles each
    user read and which users read each article."""

    __tablename__ = "user_articles"

    user_article_id = db.Column(db.Integer, 
                        autoincrement=True,
                        primary_key=True)
    user_id = db.Column(db.Integer,
                        db.ForeignKey('users.user_id'), nullable=False)
    article_id = db.Column(db.Integer,
                        db.ForeignKey('articles.article_id'), nullable=False)

class PhraseList(db.Model):
    """Stores phrases (1+ words) that the user looks up within the article."""

    __tablename__ = "wordlists"

    word_id = db.Column(db.Integer,
                        autoincrement=True,
                        primary_key=True)
    user_id = db.Column(db.Integer,
                        db.ForeignKey('users.user_id'), nullable=False)
    article_id = db.Column(db.Integer,
                        db.ForeignKey('articles.article_id'), nullable=False)
    phrase = db.Column(db.String(50), nullable=False)
    




