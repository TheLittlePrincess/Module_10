# use Flask to render a template.
# use PyMongo to interact with our Mongo database (mars_app)
# use scraping code - will convert from Jupyter notebook to Python.
from flask import Flask, render_template
from flask_pymongo import PyMongo
import scraping
# set up Flask
app = Flask(__name__)
# Use flask_pymongo to set up mongo connection
app.config["MONGO_URI"] = "mongodb://localhost:27017/mars_app"
mongo = PyMongo(app)
#define the route for the HTML page
@app.route("/")
def index():
   mars = mongo.db.mars.find_one()
   return render_template("index.html", mars=mars)
# set up our scraping route. the "button" of the web application that 
# will scrape updated data when we tell it to from the homepage of 
# the web app. It'll be tied to a button that will run the code when clicked
# Note early in the module the ipynb and py export were named Mission_to_Mars
# that is the same file refer as scraping here (change the .py file name)
@app.route("/scrape")
def scrape():
   mars = mongo.db.mars
   mars_data = scraping.scrape_all()
   mars.update({}, mars_data, upsert=True)
   return redirect('/', code=302)
#to run
if __name__ == "__main__":
   app.run()