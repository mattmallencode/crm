from flask import Flask, render_template, request, redirect, url_for, session, g
from flask_sqlalchemy import SQLAlchemy as sa
from flask_mail import Mail
from application.forms import CreateTeamForm, ContactForm, LogoutForm, LeaveTeamForm, SearchForm, DealForm
from flask_oauthlib.client import OAuth
from turbo_flask import Turbo
from config import Config
import warnings

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
        warnings.filterwarnings("ignore", module="matplotlib")
        turbo.init_app(application)
        db.init_app(application)
        application.extensions["turbo"] = turbo
        from application.modules.auth import login_required, team_required
        from application.data_models import Invites, Deals, Users, Teams, Contacts, Notes, ActivityLog, DealStageConversion
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
        # Query the db for the team_id using the cookies email.
        user = Users.query.filter_by(email=g.email).first()

        goal_closed_diagram = draw_goal_closed_diagram(user)

        try:
            deals_forecast_diagram = draw_deals_forecast_diagram(user)
        except:
            fig, ax = plt.subplots()
            plt.pie([100], colors=["#FFC154"])
            plt.title("You have no deal data. Create some deals to populate this chart", fontsize=14)
            deals_forecast_diagram = encode_diagram(plt)

        try:
            activity_diagram = draw_activity_diagram(user)
        except Exception as e:
            fig, ax = plt.subplots()
            plt.title("You have no team activity data. Get your team active to populate this chart", fontsize=13)
            plt.bar("no data", 1, color="#EC6B56")
            activity_diagram = encode_diagram(plt)
       
        #try:
        deal_stage_diagram, conversions = draw_deal_stage_diagram(user)
        #except:
        """
        fig, ax = plt.subplots()
        plt.title("You have no deal data. Create some deals to populate this chart")
        plt.barh("no data", 1, color="#EC6B56")
        plt.tight_layout()
        deal_stage_diagram = encode_diagram(plt)
        conversions=None
        """
       
        return render_template("home.html", user=user, goal_closed_diagram=goal_closed_diagram, deals_forecast_diagram=deals_forecast_diagram, activity_diagram=activity_diagram, deal_stage_diagram=deal_stage_diagram, conversions=conversions)
        
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
        plt.legend(labels=legend_labels, loc=2, bbox_to_anchor=(-0.3, 1))
        result = encode_diagram(plt)
    
        return result
    
    def draw_activity_diagram(user):
        activity = ActivityLog.query.filter_by(team_id=user.team_id)
        member_activity_count={}
        for activity in activity:
            if (activity.timestamp is not None) and (type(activity.timestamp) == datetime) and (activity.activity_type != "note"):
                if activity.timestamp.strftime("%Y-%m") == ((datetime.now() - relativedelta(months=1)).strftime("%Y-%m")):
                    if activity.actor not in member_activity_count:
                        member_activity_count[activity.actor] = 1
                    else:
                        member_activity_count[activity.actor] += 1

        # gets the top 5 most active team members
        top_team_members = sorted(member_activity_count)[:5]

        if len(top_team_members) >= 5:
            activity_range = 5
        else:
            activity_range = len(top_team_members)

        activity_count={"email":[], "task":[], "meeting":[]}
        for i in range(activity_range):
            member_activity = ActivityLog.query.filter_by(actor = top_team_members[i])
            emails=0
            tasks=0
            meetings=0
            for activity in member_activity:
                if activity.activity_type == "email":
                    emails += 1
                elif activity.activity_type == "task":
                    tasks += 1
                elif activity.activity_type == "meeting":
                    meetings += 1
            
            user = Users.query.filter_by(email=top_team_members[i]).first()
            if user.name not in top_team_members:
                top_team_members[i] = user.name
            else:
                top_team_members[i] = user.name + (" " * i)
            activity_count["email"].append(emails)
            activity_count["task"].append(tasks)
            activity_count["meeting"].append(meetings)


        fig, ax = plt.subplots()
        plt.xlabel("Activity By", fontsize=14)
        plt.ylabel("Count Of Activities", fontsize=14)

        colors = ["#47B39C", "#EC6B56", "#772953", "#FFC154"]
        bar_width=0.6
        plt.bar(top_team_members, activity_count["email"], color=colors[3], width=bar_width)
        plt.bar(top_team_members, activity_count["task"], bottom = activity_count["email"], color = colors[1], width=bar_width)
        meeting_plot = []
        for i in range(activity_range):
            meeting_plot.append(activity_count["email"][i] + activity_count["task"][i])
        plt.bar(top_team_members, activity_count["meeting"], bottom = meeting_plot, color = colors[0], width=bar_width)
        plt.legend(labels=["Emails", "Tasks", "Meetings"], loc=1, bbox_to_anchor=(1.1,1))
        result = encode_diagram(plt)
        return result
                    
    def draw_deal_stage_diagram(user):
        stages = DealStageConversion.query.filter_by(team_id = user.team_id)
        
        stage_count = {"Created":0, "Qualified To Buy":0, "Appointment Scheduled":0, "Contract Sent":0, "Closed Won":0}

        for stage in stages:
            if isinstance(stage.date, datetime):
                if stage.date.strftime("%Y-%m") == ((datetime.now() - relativedelta(months=1)).strftime("%Y-%m")):
                    if stage.stage == "Created":
                        stage_count["Created"] += 1
                    if stage.stage == "Qualified To Buy":
                        stage_count["Qualified To Buy"] += 1
                    elif stage.stage == "Appointment Scheduled":
                        stage_count["Appointment Scheduled"] += 1
                    elif stage.stage == "Contract Sent":
                        stage_count["Contract Sent"] += 1
                    elif stage.stage == "Closed Won":
                        stage_count["Closed Won"] += 1
                

        fig, ax = plt.subplots()
        plt.barh(list(stage_count.keys()), list(stage_count.values()), color = ["#FFC154", "#EC6B56", "#DC8449", "#539165", "#47B39C"])
        plt.xlabel("Number of Deals", fontsize=14)
        plt.tight_layout()
        ax.invert_yaxis()
        ax.invert_xaxis()
 
        conversions = {"Created":[0,0], "Qualified To Buy":[0,0], "Appointment Scheduled":[0,0], "Contract Sent":[0,0]}
        stage_count_values = list(stage_count.values())
        for stage in conversions:
            current_stage_index = list(stage_count).index(stage) 
            next_stage_index = current_stage_index + 1

            # calculates next step conversion
            try:
                next_step_conversion = stage_count_values[next_stage_index] / stage_count_values[current_stage_index]
                conversions[stage][0] = round(next_step_conversion * 100, 2)
            except:
                conversions[stage][0] = 0
            # calculated cumulative conversion
            try:
                cumulative_conversion = stage_count_values[next_stage_index] / stage_count_values[0]
                conversions[stage][1] = round(cumulative_conversion * 100, 2)
            except:
                conversions[stage][1] = 0
        last_v = list(stage_count.values())[-1]
        for i, v in enumerate(list(stage_count.values())):
            try:
                stage = list(stage_count.keys())[i]
                next_conversion = conversions[stage][0]
                cumulative_conversion = conversions[stage][1]
                plt.text(last_v * 0.9, i, f'Next Step Conversion: {next_conversion:.2f}%. \n Cumulative Conversion: {cumulative_conversion:.2f}%', color='black', ha='left', va='center', fontweight='bold')
            except:
                pass

        diagram = encode_diagram(plt)

        return diagram, conversions

    def encode_diagram(plt):
        buf = BytesIO()
        plt.savefig(buf, format="png")
        # encodes figure for output
        data = base64.b64encode(buf.getbuffer()).decode("ascii")
        result = f"<img src='data:image/png;base64,{data}'/>"
        return result

    return application