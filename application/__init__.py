from flask import Flask, render_template, request, redirect, url_for, session, g
from flask_sqlalchemy import SQLAlchemy as sa
from flask_mail import Mail
from application.forms import CreateTeamForm, ContactForm, LogoutForm, LeaveTeamForm, SearchForm, DealForm
from flask_oauthlib.client import OAuth
from turbo_flask import Turbo
from config import Config
turbo = Turbo()

# Set up an SQLAlchemy session for our application.
db = sa()

def create_app(config_class=Config):
    application = Flask(__name__)
    application.config.from_object(config_class)
    # Initialize Flask extensions here

    # Register blueprints here
    # oauth configuration for remote apps.
    oauth = OAuth(application)
    google = oauth.remote_app("google", content_type="application/json", consumer_key=application.config.get("GOOGLE_ID"), consumer_secret=application.config.get("GOOGLE_SECRET"), request_token_params={"scope": ["https://www.googleapis.com/auth/gmail.send", "https://www.googleapis.com/auth/gmail.readonly", "https://www.googleapis.com/auth/userinfo.email", "https://www.googleapis.com/auth/calendar.events"]}, base_url="https://www.googleapis.com/oauth2/v1/", authorize_url="https://accounts.google.com/o/oauth2/auth", access_token_method="POST", access_token_url="https://accounts.google.com/o/oauth2/token", request_token_url=None)
    # creates Mail instance for managing emails
    mail = Mail(application)
    # creates a Turbo instance

    with application.app_context():
        turbo.init_app(application)
        db.init_app(application)
        application.extensions["turbo"] = turbo
        from application.modules.auth import login_required, team_required
        from application.data_models import Invites, Deals, Users, Teams, Contacts, Notes
        from application.modules.auth import auth
        from application.modules.contacts import contacts_bp
        from application.modules.contact import contact_bp
        from application.modules.teams import teams
        from application.modules.deals import deals_bp
        application.register_blueprint(auth)
        application.register_blueprint(contacts_bp)
        application.register_blueprint(contact_bp)
        application.register_blueprint(deals_bp)
        application.register_blueprint(teams)

    @application.before_request
    def load_logged_in_user():
        """Gets user's email for the authenticated session prior to each request."""
        g.email = session.get("email", None)
        g.team_id = session.get("team_id", None)

    @application.route("/", methods=["GET", "POST"])
    @login_required
    @team_required
    def home():
        # Query the db for the team_id using the cokies email.
        user_details = Users.query.filter_by(email=g.email).first()

        return render_template("home.html", user_details=user_details)
        
    @application.route("/authorize_email/<contact_id>", methods=["GET", "POST"])
    def authorize_email(contact_id):
        """Route for getting oAuth cred's for user's gmail."""
        session["contact_id_redirect"] = contact_id
        return google.authorize(callback=url_for("authorized", _external=True))


    @application.route("/authorize_email/authorized/", methods=["GET", "POST"])
    @google.authorized_handler
    def authorized(resp):
        """Route for handling successful google oAuth."""
        if resp == None:
            resp = request.json
        contact_id_redirect = session.get("contact_id_redirect")
        session.pop("contact_id_redirect", default=None)
        session["google_token"] = (resp["access_token"],)
        user = google.get("userinfo")
        session["user_google"] = user.data["email"]
        return redirect(url_for("contact_bp.contact", contact_id=contact_id_redirect, activity="emails", _external=True))


    @google.tokengetter
    @application.route("/get_google_token", methods=["GET"])
    def get_google_token(token=None):
        """Function for fetching user's google token."""
        return session.get("google_token")

    @login_required
    @team_required
    @application.route("/save_timezone", methods=["POST"])
    def save_timezone():
        time_zone = request.form["time_zone"]
        session["time_zone"] = time_zone
        return '', 204

    return application