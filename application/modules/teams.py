from flask import Blueprint, g, render_template, current_app, session, url_for, redirect
from application.modules.auth import login_required, team_required
from application.data_models import *
from application.forms import *
from secrets import token_urlsafe
from flask_mail import Message

teams = Blueprint('teams', __name__, template_folder="templates")
mail = current_app.extensions.get("mail")
turbo = current_app.extensions.get("turbo")

@teams.route("/invite", methods=["GET", "POST"])
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


@teams.route("/create_team", methods=["GET", "POST"])
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

@teams.route("/team", methods=["GET", "POST"])
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
