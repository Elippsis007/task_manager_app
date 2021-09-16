# Importing the Flask module
# In order to use the environment variables 'env.py', we need to import the 'env' package
# MongoDB stores its data in a JSON-like format called BSON, In order to find documents from MongoDB later, we need to be able to render the ObjectId
import os
from flask import (
    Flask, flash, render_template,
    redirect, request, session, url_for)
from flask_pymongo import PyMongo
from bson.objectid import ObjectId
from werkzeug.security import generate_password_hash, check_password_hash
if os.path.exists("env.py"):
    import env 

# Create an instance of Flask, and that will be stored in a variable called 'app'

app = Flask(__name__)

# Adding configurations to my app
# Grab the database name: app.config["MONGO_DBNAME"]
# To configure the actual connection string, also called the MONGO_URI
# Grab our SECRET_KEY, which is a requirement when using some of the functions from Flask: app.secret_key = os.environ.get("SECRET_KEY")
app.config["MONGO_DBNAME"] = os.environ.get("MONGO_DBNAME")
app.config["MONGO_URI"] = os.environ.get("MONGO_URI")
app.secret_key = os.environ.get("SECRET_KEY") 


# I need to setup an instance of PyMongo, and add the app into a **Constructor Method**
# This is the Flask 'app' object I have defined above, and is the final step to ensure my Flask app is properly communicating with the Mongo database
mongo = PyMongo(app)


@app.route("/")
# The routing is a string that, when we attach it to a URL, will redirect to a particular function in our Flask app.
@app.route("/get_tasks")
def get_tasks():
    # This will find all documents from the tasks collection, and assign them to our new 'tasks' variable.
    tasks = list(mongo.db.tasks.find()) 
    # This tasks template, I want to be able to generate data from my tasks collection on MongoDB, visible to our users
    # The first 'tasks' is what the template will use, and that's equal to the second 'tasks'
    return render_template("tasks.html", tasks=tasks) 


@app.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        # check if username already exists in db
        existing_user = mongo.db.users.find_one(
            {"username": request.form.get("username").lower()})
        
        if existing_user:
            flash("Username already exists")
            return redirect(url_for("register"))

        register = {
            "username": request.form.get("username").lower(),
            "password": generate_password_hash(request.form.get("password"))
        }
        mongo.db.users.insert_one(register)

        # Put the new user into 'session' cookie
        session["user"] = request.form.get("username").lower()
        flash("Registration Successful!")
        return redirect(url_for("profile", username=session["user"]))
    
    return render_template("register.html")


@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        # check if username exists in db
        existing_user = mongo.db.users.find_one(
            {"username": request.form.get("username").lower()})

        if existing_user:
            # ensure hashed password matches user input
            if check_password_hash(
                    existing_user["password"], request.form.get("password")):
                        session["user"] = request.form.get("username").lower()
                        flash("Welcome, {}".format(
                            request.form.get("username")))
                        return redirect(url_for(
                            "profile", username=session["user"]))
            else:
                # invalid password match
                flash("Incorrect Username and/or Password")
                return redirect(url_for("login"))
                        
        else:
            # username doesn't exist
            flash("Incorrect Username and/or Password")
            return redirect(url_for("login"))

    return render_template("login.html")


@app.route("/profile/<username>", methods=["GET", "POST"])
def profile(username):
    # grab the session user's username from db
    username = mongo.db.users.find_one(
        {"username": session["user"]})["username"]

    if session["user"]:
        return render_template("profile.html", username=username)

    return redirect(url_for("login"))
                                        

@app.route("/logout")
def logout():
    # remove user from session cookie
    flash("You have been logged out")
    session.pop("user")
    return redirect(url_for("login"))


@app.route("/add_task")
def add_task():
    categories = mongo.db.categories.find().sort("category_name", 1)
    return render_template("add_task.html", categories=categories)


# The host will be set to the IP, so we need to type os.environ.get("IP") in order to fetch that default value, which was "0.0.0.0"
# The port will need to be converted to an integer, so we'll type: int(os.environ.get("PORT"))
# The final parameter will be debug=True, because during development, we want to see the actual errors that may appear, instead of a generic server warning
if __name__ == "__main__":
    app.run(host=os.environ.get("IP"),
            port=int(os.environ.get("PORT")),
            debug=True)


# I need to setup some files that Heroku needs to run the app. First, I need to tell Heroku 
# which applications and dependencies are required to run our app -> ** "pip3 freeze --local > requirements.txt" **

# the Procfile is what Heroku looks for to know which file runs the app, and how to
# run it, so use the echo command: ** "echo web: python app.py > Procfile" **