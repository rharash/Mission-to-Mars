# The first line says that we’ll use Flask to render a template.
# The second line says we’ll use PyMongo to interact with our Mongo database.
# Finally, the last line says that to use the scraping code, which we will convert from Jupyter notebook to Python.

from flask import Flask, render_template
from flask_pymongo import PyMongo
import scraping

#code to set up Flask
app = Flask(__name__)

# Use flask_pymongo to set up mongo connection(We also need to tell Python how to connect to Mongo using PyMongo.)
    #first line :tells Python that our app will connect to Mongo using a URI, a uniform resource identifier similar to a URL.
    #Second Line :is the URI we’ll be using to connect our app to Mongo. This URI is saying that the app can reach Mongo through our localhost server, using port 27017, using a database named"mars_app”.
app.config["MONGO_URI"] = "mongodb://localhost:27017/mars_app"
mongo = PyMongo(app)

#Set Up App Routes (The code we create next will set up our Flask routes: one for the main HTML page everyone will view when visiting the web app, and one to actually scrape new data using the code we’ve written.)
@app.route("/")
def index():
   mars = mongo.db.mars.find_one()
   return render_template("index.html", mars=mars)

#Following function will set up our scraping route.This route will be the “button” of the web application, the one that will scrape updated data when we tell it to from the homepage of our web app. It’ll be tied to a button that will run the code when it’s clicked.
@app.route("/scrape")
def scrape():
   mars = mongo.db.mars
   mars_data = scraping.scrape_all()
   mars.update({}, mars_data, upsert=True)
   return "Scraping Successful!"
 #The final bit of code we need for Flask is to tell it to run. Add these two lines to the bottom of your script and save your work:
if __name__ == "__main__":
   app.run()