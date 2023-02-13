from flask import Flask, render_template, request, redirect, url_for, session, g, current_app
from dotenv import load_dotenv
import os
from flask_sqlalchemy import SQLAlchemy as sa
from flask_mail import Mail, Message
from forms import SignUpForm, LoginForm, CreateTeamForm, InviteForm, ContactForm, LogoutForm, LeaveTeamForm, SearchForm, EmailForm, NoteForm, MeetingForm
from functools import wraps
from werkzeug.security import generate_password_hash, check_password_hash
from secrets import token_urlsafe
import re
from flask_oauthlib.client import OAuth
from turbo_flask import Turbo
from email.mime.text import MIMEText
import json
import base64
from datetime import datetime

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
application.config["GOOGLE_ID"] = os.environ.get("GOOGLE_ID")
application.config["GOOGLE_SECRET"] = os.environ.get("GOOGLE_SECRET")
application.config["MAIL_USE_TLS"] = False
application.config["MAIL_USE_SSL"] = True

# oauth configuration for remote apps.
oauth = OAuth(application)
google = oauth.remote_app("google", content_type="application/json", consumer_key=application.config.get("GOOGLE_ID"), consumer_secret=application.config.get("GOOGLE_SECRET"), request_token_params={"scope": ["https://www.googleapis.com/auth/gmail.send", "https://www.googleapis.com/auth/gmail.readonly", "https://www.googleapis.com/auth/userinfo.email", "https://www.googleapis.com/auth/calendar.events"]}, base_url="https://www.googleapis.com/oauth2/v1/", authorize_url="https://accounts.google.com/o/oauth2/auth", access_token_method="POST", access_token_url="https://accounts.google.com/o/oauth2/token", request_token_url=None,
                         )


# Initialize MySQL credentials from the environment variables we just loaded.
DB_HOST = os.environ.get("DB_HOST")
DB_PORT = int(os.environ.get("DB_PORT"))
DB_USER = os.environ.get("DB_USER")
DB_PASSWORD = os.environ.get("DB_PASSWORD")
DB_DB = os.environ.get("DB_DB")  # database to use.
# Set up SQLAlchemy with the above credentials.
application.config["SQLALCHEMY_DATABASE_URI"] = f"mysql+pymysql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_DB}"
# Set up an SQLAlchemy session for our application.
db = sa(application)
# creates Mail instance for managing emails
mail = Mail(application)
# creates a Turbo instance
turbo = Turbo(application)

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

    def __init__(self, invite_id=None, team_id=None):
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

    def __init__(self, contact_id=None, team_id=None, name=None, email=None, phone_number=None, contact_owner=None, company=None, status=None):
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

    def __init__(self, team_id=None, name=None):
        self.team_id = team_id
        self.name = name


class Notes(db.Model):
    note_id = db.Column(db.Integer, primary_key=True)
    contact_id = db.Column(db.String)
    note = db.Column(db.String)
    author = db.Column(db.String)
    date = db.Column(db.String)

    def __init__(self, note_id=None, contact_id=None, note=None, author=None, date=None):
        self.note_id = note_id
        self.contact_id = contact_id
        self.note = note
        self.author = author
        self.date = date


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
            return redirect(url_for("createTeam"))
        return view(**kwargs)
    return wrapped_view


@application.route("/invite", methods=["GET", "POST"])
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
            # checks if user sending invite is an admin
            if user.admin_status == False:
                form.email.errors.append(
                    "You must be an admin to invite members to your organization")
            else:
                user_to_be_invited = Users.query.filter(
                    Users.email == email).first()
                if user_to_be_invited != None:
                    if user_to_be_invited.team_id == team_id:
                        form.email.errors.append(
                            "This user is already a member of your team")
                        return render_template("invite.html", form=form, response=response)
                # collects form data and inserts into invite table
                sec = token_urlsafe(16)
                host = "http://127.0.0.1:5000"
                url = f"{host}/login/{email}_{team_id}_{sec}"
                invite.team_id = team_id
                invite.invite_id = f"{email}_{team_id}_{sec}"
                db.session.add(invite)
                db.session.commit()
                # creates email message

                msg = Message("Sherpa Invitation", sender=(
                    "Sherpa CRM", "Sherpacrm90@gmail.com"), recipients=[form.email.data])
                msg.html = f"You have been invited to join a Sherpa organisation. Click <a href = '{url}'> here</a> to join"
                # connects to mail SMTP server and sends message
                mail.connect()
                mail.send(msg)
                response = "Member has been invited"

                db.session.add(invite)
                db.session.commit()

    return render_template("invite.html", form=form, response=response)


@application.route("/", methods=["GET", "POST"])
@login_required
@team_required
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
    # Initialize the form
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
                invitation = Invites.query.filter_by(
                    invite_id=invite_id).first()
                invitation_email = invitation.invite_id.split("_")[0]
                if invitation != None and user.team_id == None and user.email == invitation_email:
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
    user = None
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


@application.route("/contacts", defaults={"filter": "all", "page": 1, "prev_sort": "None", "sort": "None", "order": "DESC", "error": "None"}, methods=["GET", "POST"])
@application.route("/contacts/<filter>/<prev_sort>/<sort>/<page>/<order>/<error>", methods=["GET", "POST"])
@login_required
@team_required
def contacts(filter, page, prev_sort, sort, order, error):
    """
    Displays list of contacts registered with this team.

    filter -- whether to show all contacts, assigned contatcs, or uanssigned contacts.
    prev_sort -- the last way the contacts were sorted e.g. NameASC (if any).
    sort -- the current way the contacts are being sorted e.g. NameDESC (if any).
    page -- the page of contacts the user wishes to view (25 contacts per page).
    order -- the order of the sort (if any), must be ASC or DESC.
    error -- error message due to form invalidation.
    """

    # Search bar.
    search_form = SearchForm()
    # Add contact form.
    add_contact = ContactForm()
    # The page the user wishes to view.
    page = int(page)
    # Must offset results from DB query to fetch the page the user is interested in.
    page_offset = (page - 1) * 25

    # Gets all contacts of user that is logged in and passes it to html template
    user = Users.query.filter_by(email=g.email).first()

    # Filters contact results
    if filter == "assigned":
        contacts = Contacts.query.filter_by(
            team_id=user.team_id, contact_owner=user.email)
    elif filter == "unassigned":
        contacts = Contacts.query.filter_by(
            team_id=user.team_id, contact_owner="")
    else:
        contacts = Contacts.query.filter_by(team_id=user.team_id)

    if search_form.validate_on_submit():
        user_search = search_form.search_bar.data
        # Before using the user's search let's optimize for it.
        optimization = optimize_search(user_search)
        # If the user is looking for an email, only search the email column.
        if optimization == "email":
            contacts = contacts.filter(Contacts.email.like(f"%{user_search}%"))
        # If the user is looking for an number, only search the number column.
        elif optimization == "number":
            contacts = contacts.filter(
                Contacts.phone_number.like(f"%{user_search}%"))
        # If the user isn't looking for an email or number definitively then search all relevant columns.
        else:
            contacts = contacts.filter(Contacts.email.like(f"%{user_search}%") | Contacts.name.like(
                f"%{user_search}%") | Contacts.company.like(f"%{user_search}%"))
    # Toggle feature of sort buttons, if the user is sorting a different column to last sort, order is ascending.
    if sort != prev_sort:
        order = "ASC"
    else:
        # User is toggling a sort they already did e.g. their second or third time clicking to sort name.
        if order == "ASC":
            order = "DESC"
        else:
            order = "ASC"
    # Only sort if the user asks us to.
    if sort != "None":
        contacts = order_contacts(sort, order, contacts)
    # Pageing functionality.
    contacts = contacts.limit(25).offset(page_offset)
    num_pages = contacts.count() // 25

    # Count the number of pages.
    if (contacts.count() % 25) > 0:
        num_pages += 1

    # Create an editable form for each contact. Will only ever 25 at a time.
    forms = []
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

    return render_template("contacts.html", forms=forms, add_contact=add_contact, search_form=search_form, contacts=contacts, num_pages=num_pages, filter=filter, page=page, prev_sort=prev_sort, sort=sort, order=order, error=error)


def optimize_search(search):
    """Report back to the caller whether the search term is likely an email, number, or otherwise."""
    if "@" in search or "." in search:
        return "email"
    if re.search('[a-zA-Z]', search) == None:
        return "number"
    else:
        return "name/company/email"


def order_contacts(sort, order, contacts):
    """Sort the results of a contacts query based on the sort (column name) and order (ASC/DESC) paramaters."""
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


@application.route("/add_contact", defaults={"filter": "all", "page": 1, "prev_sort": "None", "sort": "None", "order": "DESC", "error": "None"}, methods=["GET", "POST"])
@application.route("/add_contact/<filter>/<prev_sort>/<sort>/<page>/<order>/<error>", methods=["GET", "POST"])
@login_required
@team_required
def add_contact(filter, page, prev_sort, sort, order, error):
    """
    Add a new contact to this team.

    filter -- whether to show all contacts, assigned contatcs, or uanssigned contacts.
    prev_sort -- the last way the contacts were sorted e.g. NameASC (if any).
    sort -- the current way the contacts are being sorted e.g. NameDESC (if any).
    page -- the page of contacts the user wishes to view (25 contacts per page).
    order -- the order of the sort (if any), must be ASC or DESC.
    error -- error message due to form invalidation.
    """
    form = ContactForm()
    user = Users.query.filter_by(email=g.email).first()
    user_contacts = Contacts.query.filter_by(team_id=user.team_id)
    error = "None"
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
            # If the user's included a contact owner, check that the contact owner is a member of the organisation.
            if form.contact_owner.data != "" and Users.query.filter_by(email=form.contact_owner.data, team_id=user.team_id).first() is None:
                error = "Invalid contact owner email"
            else:
                # If the user's isn't editing the contact save changes, otherwise check that they're an admin.
                if contact.contact_owner == "" or user.admin_status == True:
                    contact.contact_owner = form.contact_owner.data

                    contact.company = form.company.data
                    contact.status = dict(
                        form.status.choices).get(form.status.data)

                    db.session.add(contact)
                    db.session.commit()
                else:
                    error = "You do not have sufficient permissions to assign a contact."
        else:
            error = "This person is already in your contacts"
    return redirect(url_for("contacts", prev_sort=prev_sort, order=order, sort=sort, page=page, filter=filter, error=error))


@application.route("/remove_contact/<contact_id>/<filter>/<prev_sort>/<sort>/<page>/<order>/<error>", methods=["GET", "POST"])
@login_required
@team_required
def remove_contact(contact_id, filter, page, prev_sort, sort, order, error):
    """
    Retrieves contact specified in parameter and removes from Contacts table.

    contact_id -- contact to be removed.
    filter -- whether to show all contacts, assigned contatcs, or uanssigned contacts.
    prev_sort -- the last way the contacts were sorted e.g. NameASC (if any).
    sort -- the current way the contacts are being sorted e.g. NameDESC (if any).
    page -- the page of contacts the user wishes to view (25 contacts per page).
    order -- the order of the sort (if any), must be ASC or DESC.
    error -- error message due to form invalidation.
    """
    contact = Contacts.query.filter_by(contact_id=contact_id).first()
    if contact is not None:
        db.session.delete(contact)
        db.session.commit()
    return redirect(url_for("contacts", prev_sort=prev_sort, order=order, sort=sort, page=page, filter=filter, error=error))


@application.route("/edit_contact", defaults={"contact_id": "None", "filter": "all", "page": 1, "prev_sort": "None", "sort": "None", "order": "DESC", "error": "None"}, methods=["GET", "POST"])
@application.route("/edit_contact/<contact_id>/<filter>/<prev_sort>/<sort>/<page>/<order>/<error>", methods=["GET", "POST"])
@login_required
@team_required
def edit_contact(contact_id, filter, page, prev_sort, sort, order, error):
    """
    Edit an existing contact in the database.

    contact_id -- contact being edited.
    filter -- whether to show all contacts, assigned contatcs, or uanssigned contacts.
    prev_sort -- the last way the contacts were sorted e.g. NameASC (if any).
    sort -- the current way the contacts are being sorted e.g. NameDESC (if any).
    page -- the page of contacts the user wishes to view (25 contacts per page).
    order -- the order of the sort (if any), must be ASC or DESC.
    error -- error message due to form invalidation.
    """
    form = ContactForm()
    error = "None"
    if form.validate_on_submit():
        user = Users.query.filter_by(email=g.email).first()
        contact = Contacts.query.filter_by(
            contact_id=contact_id, team_id=g.team_id).first()
        contact.name = form.name.data
        contact.email = form.email.data
        former_id = contact.contact_id
        contact.contact_id = f"{form.email.data}_{contact.team_id}"
        dupe_contact = None
        # If the user is editing the email of the user their contact_id will change.
        # We need to make sure they're not making a duplicate contact_id.
        if contact.contact_id != former_id:
            # If the contact_id does not already exist, this query will work and return none.
            try:
                dupe_contact = Contacts.query.filter_by(
                    contact_id=contact.contact_id).first()
            # If the contact_id already exists, this query throws an exception and we can set dupe_contact manually.s
            except:
                dupe_contact = "Duplicate!"
        # If the user isn't trying to create a duplicate contact.
        if dupe_contact == None:
            contact.phone_number = form.phone_number.data
            # If the user's editing the contact owner data, make sure they're assigning it to a valid member of their team.
            if form.contact_owner.data != "" and Users.query.filter_by(email=form.contact_owner.data, team_id=user.team_id).first() is None:
                error = "Invalid User Email"
            else:
                # If the user's isn't editing the contact save changes, otherwise check that they're an admin.
                if form.contact_owner.data == contact.contact_owner or user.admin_status == True:
                    contact.contact_owner = form.contact_owner.data
                    contact.company = form.company.data
                    contact.status = dict(
                        form.status.choices).get(form.status.data)
                    db.session.flush()
                    db.session.refresh(contact)
                    contact.contact_id = f"{form.email.data}_{g.team_id}"
                    db.session.flush()
                    db.session.commit()
                else:
                    error = "You do not have sufficient permissions to assign a contact."
        else:
            error = "Can't create a duplicate contact!"
    return redirect(url_for('contacts', prev_sort=prev_sort, order=order, sort=sort, page=page, filter=filter, error=error))


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
                form.sure_checkbox.errors.append(
                    "Can't leave a team if you own it!")
            # User isn't an owner and they confirmed, remove them from the team.
            else:
                user_details.team_id = None
                user_details.admin_status = False
                db.session.commit()
        # User didn't click the checkbox.
        else:
            form.sure_checkbox.errors.append(
                "You must click the checkbox to confirm!")
    return render_template("team.html", user_details=user_details, team=team, team_members=team_members, form=form)


@application.route("/authorize_email/<contact_id>", methods=["GET", "POST"])
def authorize_email(contact_id):
    """Route for getting oAuth cred's for user's gmail."""
    session["contact_id_redirect"] = contact_id
    return google.authorize(callback=url_for(f"authorized", _external=True))


@application.route("/authorize_email/authorized/")
@google.authorized_handler
def authorized(resp):
    """Route for handling successful google oAuth."""
    contact_id_redirect = session.get("contact_id_redirect")
    session.pop("contact_id_redirect", default=None)
    session["google_token"] = (resp["access_token"],)
    user = google.get("userinfo")
    session["user_google"] = user.data["email"]
    return redirect(url_for("contact", contact_id=contact_id_redirect, activity="emails", _external=True))


@google.tokengetter
def get_google_token(token=None):
    """Function for fetching user's google token."""
    return session.get("google_token")


@application.route("/contact/<contact_id>/<activity>", defaults={"reply": None}, methods=["GET", "POST"])
@application.route("/contact/<contact_id>/<activity>/<reply>", methods=["GET", "POST"])
@login_required
@team_required
def contact(contact_id, activity, reply):
    """
    This is the route for the contact page i.e. an individual contact, not the list.
    Calls the relevant function depending on user selection.

    <activity>
    ----------
    emails -- Sending and viewing emails to and from the contact.
    notes -- Add and view notes related to the contact.
    """
    form = EmailForm()
    if reply != None:
        reply = reply.split(",")
        form.subject.data = reply[2]
    noteForm = NoteForm()
    contact = Contacts.query.filter_by(
        contact_id=contact_id, team_id=g.team_id).first()
    google_token = session.get("google_token")
    google_email = session.get("user_google")
    if activity == "emails":
        return email_activity(google_token, form, google_email, contact_id, contact, reply)
    elif activity == "notes":
        return notes_activity(contact_id, google_token, contact)
    elif activity == "meetings":
        return meetings_activity(contact_id, google_token, contact)
    else:
        return render_template("contact.html", contact=contact, activity=activity, form=form, noteForm=noteForm, google_token=google_token, google_email=google_email)

def meetings_activity(contact_id, google_token, contact):
    form = MeetingForm()
    if google_token != None:
        pass
    # User isn't authenticated, redirect them so they can oAuth their email.
    else:
        return redirect(url_for('authorize_email', contact_id=contact_id))
    # If we can, just update the part of the page that's changed i.e. the activity box.
    if turbo.can_stream():
        return turbo.stream(turbo.update(render_template("contact_interactions.html", google_token=google_token, activity="meetings", form=form), 'activity_box'))
    else:
        return render_template("contact.html", contact=contact, google_token=google_token, activity="meetings", form=form)

def notes_activity(contact_id, google_token, contact):
    """Function for the notes activity on the contacts page."""
    response = ""
    notes = Notes.query.filter_by(contact_id=contact_id)
    noteForm = NoteForm()
    if noteForm.validate_on_submit():
        note = Notes()
        note.contact_id = contact_id
        note.note = noteForm.note.data
        note.author = g.email
        # Timestamp the note.
        note.date = datetime.now().strftime("%d/%m/%Y %H:%M")
        db.session.add(note)
        db.session.commit()
        noteForm.note.data = None
        response = "Note Added"
    # If we can, just update the part of the page that's changed i.e. the activity box.
    if turbo.can_stream():
        return turbo.stream(turbo.update(render_template("contact_interactions.html", notes=notes, google_token=google_token, contact=contact, activity="notes", noteForm=noteForm, response=response), 'activity_box'))
    else:
        return render_template("contact.html", notes=notes, contact=contact, google_token=google_token, activity="notes", noteForm=noteForm)


def email_activity(google_token, form, google_email, contact_id, contact, reply):
    """Function for the email activity on the contacts page."""
    # Make sure user has authorized their google.
    if google_token != None:
        # If the user's submitted a valid email, send the email on their behalf.
        if form.validate_on_submit():
            subject = form.subject.data
            message = form.message.data
            from_email = google_email
            to_email = contact.email
            response = send_email(
                subject, message, from_email, to_email, reply)
            # If sending the email failed, redirect them so they can oAuth their email.
            if response != 200:
                return redirect(url_for('authorize_email', contact_id=contact_id))
            reply = None
            form.subject.data = ""
            form.message.data = ""
        # Fetch this user's emails.
        response_status, threads = get_emails(
            contact.email)
        # If the fetching of the user's emails wasn't successful redirect them to re-authorize their email.
        if response_status != 200:
            return redirect(url_for('authorize_email', contact_id=contact_id))
    # User isn't authenticated, redirect them so they can oAuth their email.
    else:
        return redirect(url_for('authorize_email', contact_id=contact_id))
    # If we can, just update the part of the page that's changed i.e. the activity box.
    if turbo.can_stream():
        return turbo.stream(
            turbo.update(render_template("contact_interactions.html", contact=contact, activity="emails",
                                         google_token=google_token, form=form, google_email=google_email, threads=threads, reply=reply), 'activity_box')
        )
    else:
        return render_template("contact.html", contact=contact, activity="emails", google_token=google_token, form=form, google_email=google_email, threads=threads, reply=reply)


def send_email(subject, message, from_email, to_email, reply=None):
    """Function to send an email with an oAuth authenticated google account."""
    message = MIMEText(message)
    message["from"] = from_email
    message["to"] = to_email
    if reply != None:
        # reply[0] is the message_id we wish to reply to.
        message["in-reply-to"] = reply[0]
        # reply[0] is the message_id we wish to reply to.
        message["references"] = reply[0]
        message["message-id"] = reply[0]
        # reply[2] is the subject of the email thread we wish to reply to.
        message["subject"] = reply[2]
    else:
        message["subject"] = subject
    if reply != None:
        message = json.dumps(
            {'raw': base64.urlsafe_b64encode(message.as_bytes()).decode(), "threadId": reply[1]})
    else:
        message = json.dumps(
        {'raw': base64.urlsafe_b64encode(message.as_bytes()).decode()})
    url = f"https://gmail.googleapis.com/gmail/v1/users/{from_email}/messages/send"
    response = google.post(url, data=message, format="text")
    return response.status


def get_emails(contact_email):
    """Function to fetch any email's in the user's google from contact_email OR to contact_email."""
    # The query asks google to return all emails in the user's account TO contact_email OR FROM contact_email.
    query = f"from: {contact_email} OR to: {contact_email}"
    user_google = session.get('user_google')
    url = f"https://gmail.googleapis.com/gmail/v1/users/{user_google}/threads"
    # Get all the threads for this google account that match our query.
    response_fetch_threads = google.get(url, data={"q": query})
    # If the request failed, return the status.
    if response_fetch_threads.status != 200:
        return response_fetch_threads.status, None
    threads = []
    # For each thread returned by google.
    for thread in response_fetch_threads.data["threads"]:
        url = f"https://gmail.googleapis.com/gmail/v1/users/{user_google}/threads/{thread['id']}"
        # Fetch all the emails in that thread.
        emails = google.get(url).data
        f = open("test.json", "w")
        f.write(json.dumps(emails, indent=4))
        f.close()
        # Add the parsed emails to the threads list.
        threads.append(parse_thread(emails))
    # Sort the threads by the thread with the most recent reply.
    threads = sorted(threads, key=lambda x: max(email["timestamp"] for email in x), reverse=True)
    # Return the response status and the list of email threads.
    return (200, threads)


def parse_thread(thread):
    """Function to parse a thread of emails returned by google's API."""
    emails = []
    # For each email in this thread.
    for message in thread['messages']:
        # Set up a dictionary to represent the email.
        email = {}
        email['subject'] = None
        email['sender_email'] = None
        email['recipient_email'] = None
        email['timestamp'] = None
        email['body'] = None
        email['threadId'] = message['threadId']
        # Map each value to its appropriate header (except body.)
        for header in message['payload']['headers']:
            if header['name'].lower() == 'from':
                email['sender_email'] = header['value']
            elif header['name'].lower() == 'to':
                email['recipient_email'] = header['value']
            elif header['name'].lower() == 'subject':
                email['subject'] = header['value']
            elif header['name'].lower() == 'date':
                # Need to get rid of timezone info from timestamps.
                date_format = "%a, %d %b %Y %H:%M:%S"
                email['timestamp'] = datetime.strptime(" ".join(header['value'].split(" ")[0:-1]), date_format)
            elif header['name'].lower() == "message-id":
                email['id'] = header['value']
        # Build the body of the email and add to the dict, then append the email to this thread's list.
        email["body"] = build_email_body(message['payload'])
        emails.append(email)
    # Return the list of emails i.e. the now parsed thread.
    return emails


def build_email_body(message):
    """Method to build the body of a google api response by traversing the nested dictionaries in the JSON."""
    # If data is in the body key, we've found the content of the email's body.
    if 'data' in message['body']:
        encoded_body = message['body']['data']
        body = base64.urlsafe_b64decode(encoded_body).decode("utf-8")
        return body
    # Otherwise, traverse to the next level of the nested dictionary.
    else:
        return build_email_body(message["parts"][0])


@application.route("/reply_email/<message_id>/<thread_id>/<contact_id>/<subject>", methods=["GET", "POST"])
@login_required
@team_required
def reply_email(message_id, thread_id, contact_id, subject):
    reply = message_id + "," + thread_id + "," + subject
    return redirect(url_for("contact", contact_id=contact_id, activity="emails", reply=reply))


@application.route("/remove_note/<note_id>/<contact_id>", methods=["GET", "POST"])
@login_required
@team_required
def remove_note(note_id, contact_id):
    """This route removes the specified note for the specified contact."""
    # Fetch the note from the db.
    note = Notes.query.filter_by(note_id=note_id).first()
    # Delete the note if it exists.
    if note is not None:
        db.session.delete(note)
        db.session.commit()
    return redirect(url_for("contact", contact_id=contact_id, activity="notes"))


# Run the application in debug mode.
if __name__ == "__main__":
    application.debug = True
    application.run()
