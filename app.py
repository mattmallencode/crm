from flask import Flask, render_template, request
from dotenv import load_dotenv
import os
from flask_sqlalchemy import SQLAlchemy as sa
from flask_mail import Mail, Message
from forms import SignUpForm

application = Flask(__name__)

# initializes email configuration variables
application.config["MAIL_SERVER"] = "smtp.gmail.com"
application.config["MAIL_PORT"] = 465
application.config["MAIL_USERNAME"] = os.environ.get("MAIL_USERNAME")
application.config["MAIL_PASSWORD"] = os.environ.get("MAIL_PASSWORD")
application.config["MAIL_USE_TLS"] = False
application.config["MAIL_USE_SSL"] = True

# creates Mail instance for managing emails
mail = Mail(application)

load_dotenv()

DB_HOST = os.environ.get("DB_HOST")
DB_PORT = int(os.environ.get("DB_PORT"))
DB_USER = os.environ.get("DB_USER")
DB_PASSWORD = os.environ.get("DB_PASSWORD")

DB_DB = os.environ.get("DB_DB")

application.config["SQLALCHEMY_DATABASE_URI"] = f"mysql+pymysql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_DB}"
db = sa(application)


class Users(db.Model):
    email = db.Column(db.String, primary_key=True)
    password_hash = db.Column(db.String)
    team_id = db.Column(db.Integer)
    owner_status = db.Column(db.Boolean)
    admin_status = db.Column(db.Boolean)

class Invites(db.Model):
    invite_id = db.Column(db.String, primary_key=True)
    team_id = db.Column(db.String)

@application.route("/", methods=["GET", "POST"])
def index():
    return render_template("index.html")

@application.route("/invite", methods = ["GET", "POST"])
def invite():
    response = ""
    if request.method == "POST":
        # inserts inputted email address into Invites table along with team id
        invite = Invites()
        team_id = "xxxxxxxx"
        invite.team_id = team_id
        invite.invite_id = request.form["address"] + team_id,
        db.session.add(invite)
        db.session.commit()

        # creates email message
        msg = Message("Sherpa Invitation", sender = ("Sherpa CRM", "Sherpacrm90@gmail.com"), recipients = [request.form["address"]])
        msg.html = "You have been invited to join a Sherpa organisation. Click <a href = 'https://www.youtube.com/watch?v=dQw4w9WgXcQ'> here</a> to join"

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
    form = SignUpForm()
    return render_template("signup.html",form=form)

if __name__ == "__main__":
    application.debug = True
    application.run()