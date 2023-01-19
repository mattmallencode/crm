from flask import Flask, render_template, request
from flask_mail import Mail, Message

application = Flask(__name__)

# initializes email configuration variables
application.config["MAIL_SERVER"] = ""
application.config["MAIL_PORT"] = 465
application.config["MAIL_USERNAME"] = ""
application.config["MAIL_PASSWORD"] = ""
application.config["MAIL_USE_TLS"] = False
application.config["MAIL_USE_SSL"] = True
# creates Mail instance for managing emails
mail = Mail(application)

@application.route("/", methods=["GET", "POST"])
def index():
    return render_template("index.html")

@application.route("/invite", methods = ["GET", "POST"])
def invite():
    response = ""
    if request.method == "POST":
        # variables below will be retrieved from db
        user_id = request.form["address"]
        team_id = "21"
        link = user_id + team_id

        # creates email message
        msg = Message("Sherpa Invitation", sender = "our_email@gmail.com", recipients = ["customers@gmail.com"])
        msg.html = "You have been invited to join an organisation. Click <a href = ""> here</a> to join"

        # connects to mail SMTP server and sends message
        mail.connect()
        mail.send(msg)
        response = "Member has been invited"
    return render_template("invite.html", response = response)

if __name__ == "__main__":
    application.debug = True
    application.run()