from flask import Flask, render_template, request, redirect, url_for, session, g
from flask_sqlalchemy import SQLAlchemy as sa
from flask_mail import Mail
from application.forms import CreateTeamForm, ContactForm, LogoutForm, LeaveTeamForm, SearchForm, DealForm
from flask_oauthlib.client import OAuth
from turbo_flask import Turbo
from config import Config

import base64
from io import BytesIO
import matplotlib.pyplot as plt
import mplcyberpunk
from dateutil.relativedelta import relativedelta
from datetime import datetime

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
    google = oauth.remote_app("google", content_type="application/json", consumer_key=application.config.get("GOOGLE_ID"), consumer_secret=application.config.get("GOOGLE_SECRET"), request_token_params={"scope": ["https://www.googleapis.com/auth/gmail.send", "https://www.googleapis.com/auth/gmail.readonly", "https://www.googleapis.com/auth/userinfo.email", "https://www.googleapis.com/auth/calendar.events", "https://www.googleapis.com/auth/tasks"]}, base_url="https://www.googleapis.com/oauth2/v1/", authorize_url="https://accounts.google.com/o/oauth2/auth", access_token_method="POST", access_token_url="https://accounts.google.com/o/oauth2/token", request_token_url=None)
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
        user = Users.query.filter_by(email=g.email).first()

        goal_closed_diagram = draw_goal_closed_diagram(user)
        deals_forecast_diagram = None

        return render_template("home.html", user=user, goal_closed_diagram=goal_closed_diagram, deals_forecast_diagram=None)
        
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

    def draw_goal_closed_diagram(user):
        # Deals in the last year
        year_month_minus_one = (datetime.now() - relativedelta(years=1)).strftime("%Y-%m")
        deals = Deals.query.\
            filter(Deals.team_id == user.team_id, Deals.close_date > Deals.close_date.like(f"{year_month_minus_one}%"))
        
        buckets=[]
        for i in range(12):
            buckets.append([])
        for deal in deals:
            buckets[int(deal.close_date.strftime("%m"))].append(deal)

        closed = {"x":[], "y":[]}
        goal= {"x":[], "y":[]}

        for bucket in buckets:
            closed_sum = 0
            goal_sum = 0
            close_date = ""
            if len(bucket) != 0:
                for deal in bucket:
                    if (deal.amount is not None) and (deal.stage == "Closed Won"):
                        closed_sum += deal.amount
                    if deal.goal is not None:
                        goal_sum += deal.goal
                    close_date = deal.close_date.strftime("%Y-%m")
            
                closed["x"].append(close_date)
                closed["y"].append(closed_sum)
                goal["x"].append(close_date)
                goal["y"].append(goal_sum)
                
        
        plt.style.use("cyberpunk")
        fig, ax = plt.subplots()
        plt.xlabel("Close Date", fontsize=14)
        plt.ylabel("Closed Amount v Revenue Goal in (€) euros ", fontsize=14)
        plt.plot(closed["x"], closed["y"], marker="o", label = "Closed Amount")
        plt.plot(goal["x"], goal["y"], marker="o", label="Revenue Goal")
        plt.legend()
        
        mplcyberpunk.add_glow_effects()
           
        result = encode_diagram(plt)
        return result
    
    def draw_deals_forecast_diagram(user):
        date = datetime.now().strftime("%Y-%m")
        deals = Deals.query.\
            filter(Deals.team_id == user.team_id)
        
        data = [0,0,0,0]
        for deal in deals:
            if (deal.amount is not None) and (deal.date_created is not None):
                if deal.date_created.strftime("%Y-%m") == datetime.now().strftime("%Y-%m"):
                    if deal.stage == "Closed Won":
                        data[0] += deal.amount
                    elif deal.stage == "Appointment Scheduled":
                        data[1] += deal.amount
                    elif deal.stage == "Contract Sent":
                        data[2] += deal.amount
                    elif deal.stage == "Qualified To Buy":
                        data[3] += deal.amount

        fig, ax = plt.subplots()

        pie_labels = [f"€{value}" for value in data]
        legend_labels = ["Closed Won", "Appointment Scheduled", "Contract Sent", "Qualified To Buy"]
        explode = (0.01, 0.01, 0.01, 0.01)
        colors = ["#47B39C", "#EC6B56", "#772953", "#FFC154"]
        plt.pie(data, explode=explode, labels=pie_labels, startangle=90, colors=colors, shadow=True, autopct = "%1.1f%%", textprops={"color":"w"})
        plt.title(f"Forecasted Revenue for this month: €{sum(data)}", fontsize = 14)
        plt.legend(labels=legend_labels, loc=2)
        result = encode_diagram(plt)
    
        return result
    
    def encode_diagram(plt):
        buf = BytesIO()
        plt.savefig(buf, format="png")
        # encodes figure for output
        data = base64.b64encode(buf.getbuffer()).decode("ascii")
        result = f"<img src='data:image/png;base64,{data}'/>"
        return result


    return application