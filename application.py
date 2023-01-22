from flask import Flask, render_template, request, redirect, url_for
from dotenv import load_dotenv
import os
from flask_sqlalchemy import SQLAlchemy as sa
from flask_mail import Mail, Message
from forms import SignUpForm, LoginForm
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import LoginManager

# Initialize the flask application
application = Flask(__name__)
# Secret key for preventing CSRF attacks. 
application.config["SECRET_KEY"] = "placeholder"

# initializes email configuration variables
application.config["MAIL_SERVER"] = "smtp.gmail.com"
application.config["MAIL_PORT"] = 465
application.config["MAIL_USERNAME"] = os.environ.get("MAIL_USERNAME")
application.config["MAIL_PASSWORD"] = os.environ.get("MAIL_PASSWORD")
application.config["MAIL_USE_TLS"] = False
application.config["MAIL_USE_SSL"] = True

# creates Mail instance for managing emails
mail = Mail(application)


# Load environment variables from .env file.
load_dotenv()

# Initialize MySQL credentials from the environment variables we just loaded.
DB_HOST = os.environ.get("DB_HOST")
DB_PORT = int(os.environ.get("DB_PORT"))
DB_USER = os.environ.get("DB_USER")
DB_PASSWORD = os.environ.get("DB_PASSWORD")
DB_DB = os.environ.get("DB_DB") # database to use.
# Set up SQLAlchemy with the above credentials.
application.config["SQLALCHEMY_DATABASE_URI"] = f"mysql+pymysql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_DB}"
# Set up an SQLAlchemy session for our application.
db = sa(application)

# Users data model i.e. a representation of the users table in the database.
class Users(db.Model):
    email = db.Column(db.String, primary_key=True)
    password_hash = db.Column(db.String)
    team_id = db.Column(db.Integer)
    owner_status = db.Column(db.Boolean)
    admin_status = db.Column(db.Boolean)

'''Login form setup'''
# Creates a login_manager that lets your code and login manager work together 
login_manager = LoginManager()
# Application already exists but we can configure it to work with the login manager using the below line.
login_manager.init_app(application)
# Used to reload the user object from the user ID stored in the session. 
@login_manager.user_loader
def load_user(user_id):
    return Users.get(user_id)

class Invites(db.Model):
    invite_id = db.Column(db.String, primary_key=True)
    team_id = db.Column(db.String)

'''Login form setup'''
# Creates a login_manager that lets your code and login manager work together 
login_manager = LoginManager()
# Application already exists but we can configure it to work with the login manager using the below line.
login_manager.init_app(application)
# Used to reload the user object from the user ID stored in the session. 
@login_manager.user_loader
def load_user(user_id):
    return Users.get(user_id)

@application.route("/", methods=["GET", "POST"])
def index():
    """
    Index route for the application.
    """
    return render_template("index.html")

@application.route("/invite", methods = ["GET", "POST"])
def invite():
    """
    Route for sending an email invitation to a user for your team.
    """
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
    
@application.route("/login", methods=["GET", "POST"])
def login():
    """
    Route for authenticating a user.    
    """
    #Initialize the form 
    form = LoginForm()
    # If the user submitted the form and it passed validation 
    if form.validate_on_submit():
        # Login and validate the user
        # User needs to be an instance of your user class
        #login_user(user) 

        return render_template("login.html")

@application.route("/signup", methods=["GET", "POST"])
def signup():
    """
    Route for registering an account.
    """
    # Initialize the form
    form = SignUpForm()
    # If the user submitted the form and it passed validation.
    if form.validate_on_submit():
        email = form.email.data
        # Check that the user isn't already registered.
        if Users.query.filter_by(email=email).first() is None:
            password = form.password.data
            user = Users()
            user.email = email
            # Generate a hash for the user's password and insert credential's into the DB.
            user.password_hash = generate_password_hash(password)
            user.team_id = None
            user.admin_status = None
            user.owner_status = None
            db.session.add(user)
            db.session.commit()
            return redirect(url_for("login"))
        # If the email's already registered, inform the user.
        else:
            form.email.errors.append("That email is already registered!")
    return render_template("signup.html", form=form)

    

if __name__ == "__main__":
    application.debug = True
    application.run()
