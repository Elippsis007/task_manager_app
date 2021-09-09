import os
# Importing the Flask module
from flask import (
    Flask, flash, render_template, redirect, 
    request, session, url_for) 
# In order to use the environment variables 'env.py', we need to import the 'env' package
from flask_pymongo import PyMongo
from bson.objectid import ObjectId # MongoDB stores its data in a JSON-like format called BSON, In order to find documents from MongoDB later, we need to be able to render the ObjectId
if os.path.exists("env.py"):
    import env 

# Create an instance of Flask, and that will be stored in a variable called 'app'

app = Flask(__name__)


# Adding configurations to my app
app.config["MONGO_DBNAME"] = os.environ.get("MONGO_DBNAME") # Grab the database name: app.config["MONGO_DBNAME"]
app.config["MONGO_URI"] = os.environ.get("MONGO_URI") # To configure the actual connection string, also called the MONGO_URI
app.secret_key = os.environ.get("SECRET_KEY") # Grab our SECRET_KEY, which is a requirement when using some of the functions from Flask: app.secret_key = os.environ.get("SECRET_KEY")


# I need to setup an instance of PyMongo, and add the app into a **Constructor Method**
# This is the Flask 'app' object I have defined above, and is the final step to ensure my Flask app is properly communicating with the Mongo database
mongo = PyMongo(app) 


@app.route("/")
@app.route("/get_tasks") # The routing is a string that, when we attach it to a URL, will redirect to a particular function in our Flask app.
def get_tasks():
    tasks = mongo.db.tasks.find() # This will find all documents from the tasks collection, and assign them to our new 'tasks' variable.
    return render_template("tasks.html", tasks=tasks) # This tasks template, I want to be able to generate data from my tasks collection on MongoDB, visible to our users
                                        # The first 'tasks' is what the template will use, and that's equal to the second 'tasks',


if __name__ == "__main__":
    app.run(host=os.environ.get("IP"), # The host will be set to the IP, so we need to type os.environ.get("IP") in order to fetch that default value, which was "0.0.0.0"
            port=int(os.environ.get("PORT")), # The port will need to be converted to an integer, so we'll type: int(os.environ.get("PORT"))
            debug = True) # The final parameter will be debug=True, because during development, we want to see the actual errors that may appear, instead of a generic server warning


# I need to setup some files that Heroku needs to run the app. First, I need to tell Heroku 
# which applications and dependencies are required to run our app -> ** "pip3 freeze --local > requirements.txt" **

# the Procfile is what Heroku looks for to know which file runs the app, and how to
# run it, so use the echo command: ** "echo web: python app.py > Procfile" **