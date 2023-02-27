from flask import Blueprint, g, redirect, url_for, request, render_template, session, current_app
from werkzeug.security import generate_password_hash, check_password_hash
from functools import wraps
from application.data_models import *
from application.forms import *

auth = Blueprint('auth', __name__, template_folder="templates")
db = current_app.extensions.get("sqlalchemy")

def login_required(view):
    """Decorator that redirects a user to the login page if they're unauthenticated and trying to access a protected endpoint."""
    @wraps(view)
    def wrapped_view(**kwargs):
        if g.email is None:
            return redirect(url_for("auth.login", next=request.url))
        return view(**kwargs)
    return wrapped_view


def team_required(view):
    """Decorator that redirects a user to the login page if they're unauthenticated and trying to access a protected endpoint."""
    @wraps(view)
    def wrapped_view(**kwargs):
        if g.team_id is None:
            return redirect(url_for("teams.createTeam"))
        return view(**kwargs)
    return wrapped_view

@auth.route("/login", defaults={"invite_id": None}, methods=["GET", "POST"])
@auth.route("/login/<invite_id>", methods=["GET", "POST"])
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
            return redirect(url_for("auth.login"))
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


@auth.route("/signup", methods=["GET", "POST"])
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
            return redirect(url_for("auth.login"))
            # If the email's already registered, inform the user.
        else:
            form.email.errors.append("That email is already registered!")
    return render_template("signup.html", form=form)

@auth.route("/profile", methods=["GET", "POST"])
@login_required
@team_required
def profile():
    session.clear()
    return redirect(url_for('auth.login'))
    
