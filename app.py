from flask import Flask, render_template, request, redirect, url_for, session, g
from dotenv import load_dotenv
import os
from flask_sqlalchemy import SQLAlchemy as sa
from flask_mail import Mail, Message
from forms import SignUpForm, LoginForm, CreateTeamForm, InviteForm, ContactForm
from functools import wraps
from werkzeug.security import generate_password_hash, check_password_hash
from secrets import token_urlsafe

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

    def __init__(self, email=None, password_hash=None, team_id=None, owner_status=None, admin_status=None):
        self.email = email
        self.password_hash = password_hash
        self.team_id = team_id
        self.owner_status = owner_status
        self.admin_status = admin_status


class Invites(db.Model):
    invite_id = db.Column(db.String, primary_key=True)
    team_id = db.Column(db.Integer)

    def __init__(self, invite_id = None, team_id = None):
        self.invite_id = invite_id
        self.team_id = team_id

class Contacts(db.Model):
    contact_id = db.Column(db.String, primary_key=True)
    team_id = db.Column(db.Integer)
    name = db.Column(db.String)
    email = db.Column(db.String)
    phone_number = db.Column(db.Integer)
    contact_owner = db.Column(db.String)
    company = db.Column(db.String)
    status = db.Column(db.String)

    def __init__(self, contact_id = None, team_id = None, name = None, email = None, phone_number = None, contact_owner = None, company = None, status = None):
        self.contact_id = contact_id
        self.team_id = team_id
        self.name = name
        self.email = email
        self.phone_number = phone_number
        self.contact_owner = contact_owner
        self.company = company
        self.status = status

class Teams(db.Model):
    team_id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String)

    def __init__ (self, team_id = None, name = None):
        self.team_id = team_id
        self.name = name


@application.before_request
def load_logged_in_user():
    g.email = session.get("email", None)

def login_required(view):
    @wraps(view)
    def wrapped_view(**kwargs):
        if g.email is None:
            return redirect(url_for("login", next=request.url))
        return view(**kwargs)
    return wrapped_view

@application.route("/invite", methods = ["GET", "POST"])
@login_required
def invite():
    """
    Route for sending an email invitation to a user for your team.
    """
    form = InviteForm()
    response = ""
    if form.validate_on_submit():
        # inserts inputted email address into Invites table along with team id
        invite = Invites()
        email = form.email.data
        
        # user_id of user inviting a member
        user_id = g.email
        # checks if user sending invite is a member of an organization
        user = Users.query.filter(Users.email == user_id).first()
        team_id = user.team_id
        if user.team_id == None:
            form.email.errors.append("You are not a member of an organization")
        else:
            #checks if user sending invite is an admin
            if user.admin_status == False:
                form.email.errors.append("You must be an admin to invite members to your organization")
            else:
                user_to_be_invited = Users.query.filter(Users.email==email).first()
                if user_to_be_invited.team_id == team_id:
                    form.email.errors.append("This user is already a member of your team")
                else:
                    # collects form data and inserts into invite table
                    sec = token_urlsafe(16)
                    host = "http://127.0.0.1:5000"
                    url = f"{host}/login/{email}_{team_id}_{sec}"
                    invite.team_id = team_id
                    invite.invite_id = f"{email}_{team_id}_{sec}"

                    db.session.add(invite)
                    db.session.commit()

                    # creates email message
                    msg = Message("Sherpa Invitation", sender = ("Sherpa CRM", "Sherpacrm90@gmail.com"), recipients = [request.form["address"]])
                    msg.html = f"You have been invited to join a Sherpa organisation. Click <a href = '{url}'> here</a> to join"

                    # connects to mail SMTP server and sends message
                    mail.connect()
                    mail.send(msg)
                    response = "Member has been invited"
                    
                    db.session.add(invite)
                    db.session.commit()
  
    return render_template("invite.html", form = form, response = response)

@application.route("/", methods=["GET", "POST"])
@login_required
def home():
    # Query the db for the team_id using the cokies email.
    user_details = Users.query.filter_by(email=g.email).first()

        
    return render_template("home.html", user_details=user_details)

@application.route("/login", defaults={"invite_id": None}, methods=["GET", "POST"])
@application.route("/login/<invite_id>", methods=["GET", "POST"])
def login(invite_id):
    """
    Route for authenticating a user.    
    """
    # The login page fails when logging in without signing up
    #Initialize the form 
    form = LoginForm()
    email = form.email.data

    # If the user submitted the form and it passed validation 
    if form.validate_on_submit():
        user = Users.query.filter_by(email=email).first()
        # If the user does not exist take them to signup page
        if user is None:
            form.email.errors.append("Incorrect email / password!")
            return redirect(url_for("login"))

        elif user is not None and check_password_hash(user.password_hash, form.password.data):
            session.clear()
            session["email"] = email
            next_page = request.args.get("next")
            if not next_page:
                next_page = url_for("home")
            if invite_id != None:
                user = Users.query.filter_by(email=email).first()
                invitation = Invites.query.filter_by(invite_id=invite_id).first()
                invitation_email = invitation.invite_id.split("_")[0]
                print(invitation_email)
                if  invitation != None and user.team_id == None and user.email == invitation_email:
                    user.team_id = invitation.team_id
                    user.admin_status = True
                    user.owner_status = True
                    db.session.delete(invitation)
                    db.session.commit()
            return redirect(next_page)
        else:
            form.email.errors.append("Incorrect email / password!")
        # Login and validate the user
        # User needs to be an instance of your user class
    return render_template("login.html", form=form)

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

@application.route("/create_team", methods=["GET", "POST"])
@login_required
def createTeam():
    """
    Route for registering an team.
    """
    form = CreateTeamForm()
    if form.validate_on_submit():
        # checks if user is already a member of a team
        user = Users.query.filter_by(email=g.email).first()
        if user.team_id is None:
            team = Teams()
            team.name = form.name.data

            # team inserted into database and assigned unique id
            db.session.add(team)
            db.session.flush()
            # team object is refreshed with team id now accessible
            db.session.refresh(team)
           
            # updates users admin and owner status in Users table
            user.admin_status = True
            user.owner_status = True
            user.team_id = team.team_id

            # commits changes to database
            db.session.commit()

            return redirect(url_for("home"))
        else:
            form.name.errors.append("You are already a member of a team")
    return render_template("create_team.html", form=form)


@application.route("/contacts", methods =["GET", "POST"])
@login_required
def contacts():
    form = ContactForm()
    # gets all contacts of user that is logged in and passes it to html template
    user = Users.query.filter_by(email=g.email).first()
    contacts = Contacts.query.filter_by(team_id=user.team_id)
    return render_template("contacts.html", form = form, contacts = contacts)

@application.route("/add_contact", methods = ["GET", "POST"])
@login_required
# allows a user to add contacts to their contact list
def add_contact():
    form = ContactForm()
    if form.validate_on_submit():
        user = Users.query.filter_by(email=g.email).first()
        #  checks if contact being added belongs to user's organization already
        if Contacts.query.filter_by(email=form.email.data, team_id=user.team_id).first() is None:
            team_id = user.team_id

            contact = Contacts()
            contact.contact_id = f"{form.email.data}_{team_id}"
            contact.team_id = team_id
            contact.name = form.name.data
            contact.email = form.email.data
            contact.phone_number = form.phone_number.data
            contact.contact_owner = form.contact_owner.data
            contact.company = form.company.data
            contact.status = dict(form.status.choices).get(form.status.data)

            db.session.add(contact)
            db.session.commit()
            return redirect(url_for("contacts"))
        else:
            form.name.errors.append("This person is already in your contacts")
    return render_template("add_contact.html", form = form)


@application.route("/remove_contact/<contact_id>", methods = ["GET", "POST"])
@login_required
def remove_contact(contact_id):
    # retrieves contact specified in parameter and removes from Contacts database
    contact = Contacts.query.filter_by(contact_id = contact_id).first()
    if contact is not None:
        db.session.delete(contact)
        db.session.commit()
    return redirect(url_for("contacts"))

@application.route("/edit_contact/<contact_id>", methods=["GET", "POST"])
@login_required
def edit_contact(contact_id):
    form = ContactForm()
    
    contact = Contacts.query.filter_by(contact_id = contact_id).first()
    contact.name = form.name.data
    contact.email = form.email.data
    contact.phone_number = form.phone_number.data
    contact.contact_owner = form.contact_owner.data
    contact.company = form.company.data
    contact.status = dict(form.status.choices).get(form.status.data)
    db.session.flush()
    db.session.commit()

    return redirect(url_for('contacts'))

if __name__ == "__main__":
    application.debug = True
    application.run()