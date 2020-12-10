from flask import Flask, render_template, redirect
from flask_pymongo import PyMongo
import scrape_mars

# Create an instance of Flask
app = Flask(__name__)

# Use PyMongo to establish Mongo connection
mongo = PyMongo(app, uri="mongodb://localhost:27017/app")


@app.route("/")
def home():

    # Find one record of data from the mongo database
    destination_data = mongo.db.collection.find_one()

    # return template and data
    return render_template("index.html", mars=destination_data)


# Create a route called `/scrape` that will import your `scrape_mars.py` script and 
# call your `scrape` function. Store the return value in Mongo as a Python dictionary.
# Route that will trigger the scrape function
@app.route("/scrape")
def scrape():

    # Run the scrape function
    mars_data = scrape_mars.scrape_info()

    # Update the Mongo database using update and upsert=True
    mongo.db.collection.update({}, mars_data, upsert=True)

    # Redirect back tp home page
    return redirect("/")


# Create a root route `/` that will query your Mongo database and pass the 
# mars data into an HTML template to display the data.
# Route to render index.html template using data from Mongo



# Create a template HTML file called `index.html` that will take the mars data dictionary 
# and display all of the data in the appropriate HTML elements.
