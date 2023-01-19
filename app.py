from flask import Flask, render_template, request
from dotenv import load_dotenv
import os

load_dotenv()

application = Flask(__name__)
DB_HOST = os.environ.get("DB_HOST")
DB_PORT = os.environ.get("DB_PORT")
DB_USER = os.environ.get("DB_USER")
DB_PASSWORD = os.environ.get("DB_PASSWORD")

@application.route("/", methods=["GET", "POST"])
def index():
    return render_template("index.html")

def home():
    if request.method == "POST":
        print(request.form["name"])
        print(request.form["email"])
        return 

    return render_template("home.html")
if __name__ == "__main__":
    application.debug = True
    application.run()