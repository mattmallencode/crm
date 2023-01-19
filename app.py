from flask import Flask, render_template
application = Flask(__name__)


@application.route("/", methods=["GET", "POST"])
def index():
    return render_template("index.html")

@ application.route("/login", methods=["GET", "POST"])
def login():
    return render_template("login.html")

@ application.route("/signup", methods=["GET", "POST"])
def signup():
    return render_template("signup.html")

if __name__ == "__main__":
    application.debug = True
    application.run()