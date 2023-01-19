from flask import Flask, render_template, request
application = Flask(__name__)


@application.route("/", methods=["GET", "POST"])
def index():
    return render_template("index.html")

def home():
    if request.method == "POST":
        print(request.form["name"])
        print(request.form["email"])
        return 

    return render_template("home.html")
if __name__ == "__main__":
    application.debug = True
    application.run()