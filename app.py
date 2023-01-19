from flask import Flask, render_template, request
from dotenv import load_dotenv
import os
from flask_mail import Mail, Message
# initializes email configuration variables
application.config["MAIL_SERVER"] = ""
application.config["MAIL_PORT"] = 465
application.config["MAIL_USERNAME"] = ""
application.config["MAIL_PASSWORD"] = ""
application.config["MAIL_USE_TLS"] = False
application.config["MAIL_USE_SSL"] = True

# creates Mail instance for managing emails
mail = Mail(application)

load_dotenv()

application = Flask(__name__)
DB_HOST = os.environ.get("DB_HOST")
DB_PORT = os.environ.get("DB_PORT")
DB_USER = os.environ.get("DB_USER")
DB_PASSWORD = os.environ.get("DB_PASSWORD")

@application.route("/", methods=["GET", "POST"])
def index():
    return render_template("index.html")

@application.route("/invite", methods = ["GET", "POST"])
def invite():
    response = ""
    if request.method == "POST":
        # variables below will be retrieved from db
        user_id = request.form["address"]
        team_id = "21"
        link = user_id + team_id

        # creates email message
        msg = Message("Sherpa Invitation", sender = "our_email@gmail.com", recipients = ["customers@gmail.com"])
        msg.html = "You have been invited to join an organisation. Click <a href = ""> here</a> to join"

        # connects to mail SMTP server and sends message
        mail.connect()
        mail.send(msg)
        response = "Member has been invited"
    return render_template("invite.html", response = response)

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