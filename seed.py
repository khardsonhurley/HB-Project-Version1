"""Utility file to seed the articles database from newspaper API"""

from sqlalchemy import func
from model import (Article, Category)
from server import app, db, connect_to_db
import newspaper

def load_articles():
    """Load articles into articles table. Adds categories to categories table."""
    
    category_urls = ['http://politica.elpais.com', 'http://one.elpais.com',
    'http://deportes.elpais.com','http://escuela.elpais.com', 
    'http://cultura.elpais.com', 'http://motor.elpais.com', 
    'http://programacion-tv.elpais.com', 
    'http://smoda.elpais.com', 'http://resultados.elpais.com', 
    'http://internacional.elpais.com', 'http://tecnologia.elpais.com', 
    'http://elpaissemanal.elpais.com', 'http://elviajero.elpais.com', 
    'http://economia.elpais.com', 'http://elcomidista.elpais.com']


    category_dict = {'politica':'Politics', 
                 'one': 'Media',
                 'deportes': 'Sports',
                 'escuela': 'Education',
                 'cultura': 'Culture',
                 'smoda': 'Fashion',
                 'resultados': 'Olympics',
                 'internacional': 'International',
                 'technologia':'Technology',
                 'elpaissemanal':'Weekly News',
                 'elviajero': 'Travel',
                 'elcomidista':'Food'
                 }

    for url in category_urls:
        #creates a newspaper object. 
        category_newspaper = newspaper.build(url, memoize_articles=False)
        #gets the category code from the url. 
        category_name = url[7:-11]
        
        #Queries for the category in the database. 
        # result = Category.query.filter_by(category_code=category_name)

        # #If the category is not already in the database, adds 
        # #to the categories table.
        # """THIS ISNT WORKING!!!!!! HELP!!!!!!"""
        # # if not result: 

        #Adds category to the database in the categories table. 
        db_category = Category(category_code=category_name, url=url,
                            english_category=category_dict[category_name])

        #Verifying that the category has been added. 
        db.session.add(db_category)
        db.session.commit()

        print "\n\n\n\n\nAdded category %s \n\n\n\n\n" % (category_name)
        
        #creates a list of article objects. 
        category_articles = category_newspaper.articles

        ########SLIDE THIS LIST ^^^^^ TO GET FIRST 100######

        #iterates over the list of article objects. 
        for article in category_articles:
            #downloads and parses through the article. 
            article.download()
            print 'after download'
            article.parse()
            print 'after parse'

            #instantiates an instance in the articles table. 
            db_article = Article(mainsite=url, title=article.title, 
                            authors=article.authors, language='es',
                            url=article.url, category_code=category_name, 
                            top_image=article.top_image)

            #adds the article content to the database. 
            db.session.add(db_article)
            db.session.commit()
            #Verifying article is committed. 
            print "commited %s" % (db_article)
            
    
        


# def load_users():
#     """Load users from u.user into database"""

#     for i, row in enumerate(open("seed_data/u.user")):
#         row = row.rstrip()
#         user_id, age, gender, occupation, zipcode = row.split("|")


###################### HELPER FUNCTIONS ########################


if __name__ == "__main__":
    connect_to_db(app)
    db.create_all()
    load_articles()
   