from flask import Flask, render_template, request, redirect, url_for, session, g
from dotenv import load_dotenv
import os
from flask_sqlalchemy import SQLAlchemy as sa
from flask_mail import Mail, Message
from forms import SignUpForm, LoginForm, CreateTeamForm, InviteForm, ContactForm, LogoutForm, LeaveTeamForm, SearchForm
from functools import wraps
from werkzeug.security import generate_password_hash, check_password_hash
from secrets import token_urlsafe
import re

# Load environment variables from .env file.
load_dotenv()

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
# creates Mail instance for managing emails
mail = Mail(application)

# Users data model i.e. a representation of the users table in the database.
class Users(db.Model):
    email = db.Column(db.String, primary_key=True)
    password_hash = db.Column(db.String)
    team_id = db.Column(db.Integer)
    owner_status = db.Column(db.Boolean)
    admin_status = db.Column(db.Boolean)
    name = db.Column(db.String)

    def __init__(self, email=None, password_hash=None, team_id=None, owner_status=None, admin_status=None, name=None):
        self.email = email
        self.password_hash = password_hash
        self.team_id = team_id
        self.owner_status = owner_status
        self.admin_status = admin_status
        self.name = name

# Invites data model i.e. a representation of the users table in the database.
class Invites(db.Model):
    invite_id = db.Column(db.String, primary_key=True)
    team_id = db.Column(db.Integer)

    def __init__(self, invite_id = None, team_id = None):
        self.invite_id = invite_id
        self.team_id = team_id

# Contacts data model i.e. a representation of the contacts table in the database.
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

# Teams data model i.e. a representation of the teams table in the database.
class Teams(db.Model):
    team_id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String)

    def __init__ (self, team_id = None, name = None):
        self.team_id = team_id
        self.name = name

@application.before_request
def load_logged_in_user():
    """Gets user's email for the authenticated session prior to each request."""
    g.email = session.get("email", None)
    g.team_id = session.get("team_id", None)

def login_required(view):
    """Decorator that redirects a user to the login page if they're unauthenticated and trying to access a protected endpoint."""
    @wraps(view)
    def wrapped_view(**kwargs):
        if g.email is None:
            return redirect(url_for("login", next=request.url))
        return view(**kwargs)
    return wrapped_view

def team_required(view):
    """Decorator that redirects a user to the login page if they're unauthenticated and trying to access a protected endpoint."""
    @wraps(view)
    def wrapped_view(**kwargs):
        if g.team_id is None:
            return redirect(url_for("home"))
        return view(**kwargs)
    return wrapped_view


@application.route("/invite", methods = ["GET", "POST"])
@login_required
@team_required
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
                if user_to_be_invited != None:
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

                    msg = Message("Sherpa Invitation", sender = ("Sherpa CRM", "Sherpacrm90@gmail.com"), recipients = [form.email.data])
                    msg.html = f"You have been invited to join a Sherpa organisation. Click <a href = '{url}'> here</a> to join"#
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
                if  invitation != None and user.team_id == None and user.email == invitation_email:
                    user.team_id = invitation.team_id
                    user.admin_status = False
                    user.owner_status = False
                    db.session.delete(invitation)
                    db.session.commit()
            session["team_id"] = user.team_id
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
            user.name = form.name.data
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
    user=None
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
            session["team_id"] = user.team_id
            g.team_id = session.get("team_id")
            return redirect(url_for("home"))
        else:
            form.name.errors.append("You are already a member of a team")
    return render_template("create_team.html", form=form, user=user)


@application.route("/contacts", defaults={"filter":"all", "page":1, "prev_sort": "None", "sort": "None", "order": "DESC"} , methods =["GET", "POST"])
@application.route("/contacts/<filter>/<prev_sort>/<sort>/<page>/<order>", methods =["GET", "POST"])
@login_required
@team_required
def contacts(filter, page, prev_sort, sort, order):
    # nameASC
    # Order By name ASC
    # <Button>
    search_form = SearchForm()
    form2 = ContactForm()
    page = int(page)
    page_offset = (page - 1) * 25

    # gets all contacts of user that is logged in and passes it to html template
    user = Users.query.filter_by(email=g.email).first()

    # Filters contact results 
    if filter == "assigned":
        contacts = Contacts.query.filter_by(team_id=user.team_id, contact_owner=user.email)
    elif filter == "unassigned":
        contacts = Contacts.query.filter_by(team_id=user.team_id, contact_owner="")
    else:
        contacts = Contacts.query.filter_by(team_id=user.team_id)
        
    if search_form.validate_on_submit():
        user_search = search_form.search_bar.data
        optimization = optimize_search(user_search)
        if optimization == "email":
            contacts = contacts.filter(Contacts.email.like(f"%{user_search}%"))
        elif optimization == "number":
            contacts = contacts.filter(Contacts.phone_number.like(f"%{user_search}%"))
        else:
            contacts = contacts.filter(Contacts.email.like(f"%{user_search}%") | Contacts.name.like(f"%{user_search}%") | Contacts.company.like(f"%{user_search}%"))
    if sort != prev_sort:
        order="ASC"
    else:
        if order == "ASC":
            order = "DESC"
        else:
            order = "ASC"
    if sort != "None": 
        contacts = order_contacts(sort, order, contacts)
    contacts = contacts.limit(25).offset(page_offset)
    num_pages = contacts.count() // 25
    
    if (contacts.count() % 25) > 0:
        num_pages += 1
    
    forms=[]
    for contact in contacts:
        form = ContactForm()
        form.contact_id.data = contact.contact_id
        form.name.data = contact.name
        form.email.data = contact.email
        form.phone_number.data = contact.phone_number
        form.contact_owner.data = contact.contact_owner
        form.company.data = contact.company
        form.status.data = contact.status
        forms.append(form) 

    return render_template("contacts.html", forms = forms, form2 = form2, search_form = search_form, contacts = contacts, page = page, filter=filter, num_pages = num_pages)
    

def optimize_search(search):
    if "@" in search or "." in search:
        return "email"
    if re.search('[a-zA-Z]', search) == None:
        return "number"
    else:
        return "name/company/email"

def order_contacts(sort, order, contacts):
    if sort == "name":
        if order == "ASC":
            contacts = contacts.order_by(Contacts.name)
        else:
            contacts = contacts.order_by(Contacts.name.desc())
    elif sort == "email":
        if order == "ASC":
            contacts = contacts.order_by(Contacts.email)
        else:
            contacts = contacts.order_by(Contacts.email.desc())
    elif sort == "phone_number":
        if order == "ASC":
            contacts = contacts.order_by(Contacts.phone_number)
        else:
            contacts = contacts.order_by(Contacts.phone_number.desc())
    elif sort == "contact_owner":
        if order == "ASC":
            contacts = contacts.order_by(Contacts.contact_owner)
        else:
            contacts = contacts.order_by(Contacts.contact_owner.desc())
    elif sort == "company":
        if order == "ASC":
            contacts = contacts.order_by(Contacts.company)
        else:
            contacts = contacts.order_by(Contacts.company.desc())
    elif sort == "status":
        if order == "ASC":
            contacts = contacts.order_by(Contacts.status)
        else:
            contacts = contacts.order_by(Contacts.status.desc())
    return contacts

@application.route("/add_contact", methods = ["GET", "POST"])
@login_required
@team_required
# allows a user to add contacts to their contact list
def add_contact():
    form = ContactForm()
    user = Users.query.filter_by(email=g.email).first()
    user_contacts = Contacts.query.filter_by(team_id=user.team_id)
    if form.validate_on_submit():
        #  checks if contact being added belongs to user's organization already
        if Contacts.query.filter_by(email=form.email.data, team_id=user.team_id).first() is None:
            team_id = user.team_id

            contact = Contacts()
            contact.contact_id = f"{form.email.data}_{team_id}"
            contact.team_id = team_id
            contact.name = form.name.data
            contact.email = form.email.data
            contact.phone_number = form.phone_number.data
            if form.contact_owner.data != "" and Users.query.filter_by(email=form.contact_owner.data, team_id=user.team_id).first() is None:
                form.contact_owner.errors.append("Invalid user email")
            else:
                if contact.contact_owner == "" or ((user.owner_status == True) and (user.admin_status == True)):
                    contact.contact_owner = form.contact_owner.data

                    contact.company = form.company.data
                    contact.status = dict(form.status.choices).get(form.status.data)

                    db.session.add(contact)
                    db.session.commit()
                else:
                    form.contact_owner.errors.append("You do not have sufficient permissions to assign a contact.")
        else:
            form.name.errors.append("This person is already in your contacts")
    return redirect(url_for("contacts"))


@application.route("/remove_contact/<contact_id>", methods = ["GET", "POST"])
@login_required
@team_required
def remove_contact(contact_id):
    print(contact_id)
    # retrieves contact specified in parameter and removes from Contacts database
    contact = Contacts.query.filter_by(contact_id=contact_id).first()
    if contact is not None:
        db.session.delete(contact)
        db.session.commit()
    return redirect(url_for("contacts"))

@application.route("/edit_contact/<contact_id>", methods=["GET", "POST"])
@login_required
@team_required
def edit_contact(contact_id):
    form = ContactForm()
    print(contact_id)
    if form.validate_on_submit():
        user = Users.query.filter_by(email=g.email).first()

        contact = Contacts.query.filter_by(contact_id=contact_id, team_id=g.team_id).first()
        contact.name = form.name.data
        contact.email = form.email.data
        former_id = contact.contact_id
        contact.contact_id = f"{form.email.data}_{contact.team_id}"
        dupe_contact = None
        if contact.contact_id != former_id:
            try:
                dupe_contact = Contacts.query.filter_by(contact_id = contact.contact_id).first()
            except:
                dupe_contact = "Duplicate!"
        if dupe_contact == None:
            contact.phone_number = form.phone_number.data
            if form.contact_owner.data != "" and Users.query.filter_by(email=form.contact_owner.data, team_id=user.team_id).first() is None:
                form.contact_owner.errors.append("Invalid user email")
            else:
                if form.contact_owner.data == contact.contact_owner or ((user.owner_status == True) and (user.admin_status == True)):
                    contact.contact_owner = form.contact_owner.data
                    contact.company = form.company.data
                    contact.status = dict(form.status.choices).get(form.status.data)
                    #contact.status.choices.default
                    db.session.flush()
                    db.session.refresh(contact)

                    contact.contact_id = f"{form.email.data}_{g.team_id}"
                    db.session.flush()
                    db.session.commit()
                else:
                    form.contact_owner.errors.append("You do not have sufficient permissions to assign a contact.")
        else:
            form.contact_owner.errors.append("Can't create a duplicate contact!")
        return redirect(url_for('contacts'))

@application.route("/profile", methods=["GET", "POST"])
@login_required
@team_required
def profile():
    """Route for viewing profile information and logging out."""
    form = LogoutForm()
    # If user clicked log out, then clear their session's cookies and redirect to login.
    if form.validate_on_submit():
        session.clear()
        return redirect(url_for('login'))
    user = Users.query.filter_by(email=g.email).first()
    team = Teams.query.filter_by(team_id=user.team_id).first()
    return render_template("profile.html", form=form, user=user, team=team)


@application.route("/team", methods=["GET", "POST"])
@login_required
@team_required
def team():
    """Route for viewing team members, links to inviting team members (if admin), and allows leaving teams."""
    form = LeaveTeamForm()
    user_details = Users.query.filter_by(email=g.email).first()
    team = Teams.query.filter_by(team_id=user_details.team_id).first()
    team_members = Users.query.filter_by(team_id=user_details.team_id).all()
    if form.validate_on_submit():
        # User must click a confirmation checkbox.
        if form.sure_checkbox.data == True:
            # If the user is an owner, don't let them leave.
            if user_details.owner_status == True:
                form.sure_checkbox.errors.append("Can't leave a team if you own it!")
            # User isn't an owner and they confirmed, remove them from the team.
            else:
                user_details.team_id = None
                user_details.admin_status = False
                db.session.commit()
        # User didn't click the checkbox.
        else:
            form.sure_checkbox.errors.append("You must click the checkbox to confirm!")
    return render_template("team.html", user_details=user_details, team=team, team_members=team_members, form=form)
    

if __name__ == "__main__":
    application.debug = True
    application.run()