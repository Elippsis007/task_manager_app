import os
from flask import Flask # Importing the Flask module
# In order to use the environment variables 'env.py', we need to import the 'env' package
if os.path.exists("env.py"):
    import env 

# Create an instance of Flask, and that will be stored in a variable called 'app'

app = Flask(__name__)


@app.route("/")
def hello():
    return "Hello World....again"


if __name__ == "__main__":
    app.run(host=os.environ.get("IP"), # The host will be set to the IP, so we need to type os.environ.get("IP") in order to fetch that default value, which was "0.0.0.0"
            port=int(os.environ.get("PORT")), # The port will need to be converted to an integer, so we'll type: int(os.environ.get("PORT"))
            debug = True) # The final parameter will be debug=True, because during development, we want to see the actual errors that may appear, instead of a generic server warning

            