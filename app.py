from flask import Flask, render_template, request
from dotenv import load_dotenv
import os
import pymysql

load_dotenv()

application = Flask(__name__)
DB_HOST = os.environ.get("DB_HOST")
DB_PORT = int(os.environ.get("DB_PORT"))
DB_USER = os.environ.get("DB_USER")
DB_PASSWORD = os.environ.get("DB_PASSWORD")

DB_DB = os.environ.get("DB_DB")

DB_CONNECTION = pymysql.connect(
    host=DB_HOST,
    port=DB_PORT,
    user=DB_USER,
    password=DB_PASSWORD,
    db=DB_DB
)

@application.route("/", methods=["GET", "POST"])
def index():
    return render_template("index.html")

def home():
    if request.method == "POST":
        print(request.form["name"])
        print(request.form["email"])
        return 

    return render_template("home.html")
    
@ application.route("/login", methods=["GET", "POST"])
def login():
    return render_template("login.html")

@ application.route("/signup", methods=["GET", "POST"])
def signup():
    return render_template("signup.html")

if __name__ == "__main__":
    application.debug = True
    application.run()