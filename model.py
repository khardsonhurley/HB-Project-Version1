"""Models and database functions for Parrot"""


#allows me to use the session object
from flask_sqlalchemy import SQLAlchemy 

db = SQLAlchemy()

################################################################################
#Model definitions (MVP)

class User(db.Model):
    """User of Parrot website"""

    __tablename__ = "users"

    user_id = db.Column(db.Integer, 
                        autoincrement=True,
                        primary_key=True)
    email = db.Column(db.String(50), nullable=True, unique=True)
    username = db.Column(db.String(50), nullable=False, unique=True)
    password = db.Column(db.String(15), nullable=True)
    first_name = db.Column(db.String(50),nullable=True)
    last_name = db.Column(db.String(50),nullable=True)
    phone = db.Column(db.String(20), nullable=True)
    #Here will auto seed Spanish until enable other language features. 
    language = db.Column(db.String(20),nullable=True)
    #Consult language proficiency resource
    language_level = db.Column(db.String(15),nullable=True)
  
    ##### Relationships #####
    #Note that from the articles table if you call on 'users' it will return a
    #list of article objects for that user. 
    article = db.relationship('Article', secondary= 'user_articles', backref= 'users')

class Article(db.Model):
    """Articles available to users."""

    __tablename__ = "articles"

    article_id = db.Column(db.Integer, 
                        autoincrement=True,
                        primary_key=True)
    title = db.Column(db.String(100), nullable=True)
    author= db.Column(db.String(50), nullable=True)
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
    article_id = db.Column(db.Integer,
                        db.ForeignKey('articles.article_id'), nullable=False)
    user_id = db.Column(db.Integer,
                        db.ForeignKey('users.user_id'), nullable=False)


class Phrase(db.Model):
    """Stores phrases (1+ words) that the user looks up within the article."""

    __tablename__ = "phrases"

    phrase_id = db.Column(db.Integer,
                        autoincrement=True,
                        primary_key=True)
    user_id = db.Column(db.Integer,
                        db.ForeignKey('users.user_id'), nullable=False)
    article_id = db.Column(db.Integer,
                        db.ForeignKey('articles.article_id'), nullable=False)
    phrase = db.Column(db.String(400), nullable=False)
    translation = db.Column(db.String(400), nullable=False)
    
    ##### Relationships #####
    article = db.relationship('Article', backref='phrases')
    user = db.relationship('User', backref='phrases')

class Note(db.Model):
    """Stores the notes a user makes when reading an article."""

    __tablename__ = "notes"

    notes_id = db.Column(db.Integer,
                        autoincrement=True,
                        primary_key=True)
    user_id = db.Column(db.Integer,
                        db.ForeignKey('users.user_id'), nullable=False)
    article_id = db.Column(db.Integer,
                        db.ForeignKey('articles.article_id'), nullable=False)

    text = db.Column(db.Text, nullable=True)

    ##### Relationships #####

    #Note that from the articles table if you call on 'notes' it will return a
    #list of notes for that particular article. 
    article = db.relationship('Article', backref='notes')

    #Note that from the users table if you call on 'notes' it will return a
    #list of notes for that particular article. 
    user = db.relationship('User', backref='notes')



################################################################################
#Model definitions (2.0 Features)

# class Channel(db.Model):
#     """Channels shown in articles"""

#     __tablename__ = "channels"

#     channel_id = db.Column(db.Integer,
#                         autoincrement=True,
#                         primary_key=True)
#     channel_name = db.Column(db.String(20), nullable=False)

# class Comments(db.Model):
#     """Stores comments made by user in each channel"""
    
#     __tablename__ = "comments"

#     comment_id = db.Column(db.Integer,
#                         autoincrement=True,
#                         primary_key=True)
#     user_id = db.Column(db.Integer,
#                         db.ForeignKey('users.user_id'), nullable=False)
#     article_id = db.Column(db.Integer,
#                         db.ForeignKey('articles.article_id'), nullable=False)
#     channel_id = db.Column(db.Integer,
#                         db.ForeignKey('channels.channel_id'), nullable=False)
#     phrase_id = db.Column(db.Integer,
#                         db.ForeignKey('phrases.phrase_id'), nullable=False)
#     comment = db.Column(db.Text, nullable=False)

#     article = db.relationship("Article")


#####################################################################
# Helper functions

def connect_to_db(app):
    """Connect the database to our Flask app."""

    # Configure to use our PostgreSQL database
    app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///parrot'
    db.app = app
    db.init_app(app)


if __name__ == "__main__":

    from server import app
    connect_to_db(app)
    print "Connected to DB."




