import flask_unittest
import unittest
from flask import Flask, render_template, request, redirect, url_for, session, g
from dotenv import load_dotenv
import os
from flask_sqlalchemy import SQLAlchemy as sa
from flask_mail import Mail, Message
from forms import SignUpForm, LoginForm, CreateTeamForm, InviteForm, addContactForm
from functools import wraps
from werkzeug.security import generate_password_hash, check_password_hash
from secrets import token_urlsafe
from application import Users

from flask.testing import FlaskClient
from flask.wrappers import Response
from flask.globals import g, session, request
from bs4 import BeautifulSoup

class TestBasics(flask_unittest.ClientTestCase):
    """Setting up functions which will be used across the other testcses
    Allows for common properties """
    def create_app(self):
        # Create an instnace of the application 
        # Initialize the flask application
        self.application = Flask(__name__)
        # Secret key for preventing CSRF attacks. 
        self.application.config["SECRET_KEY"] = "placeholder"

        # initializes email configuration variables
        self.application.config["MAIL_SERVER"] = "smtp.gmail.com"
        self.application.config["MAIL_PORT"] = 465
        self.application.config["MAIL_USERNAME"] = os.environ.get("MAIL_USERNAME")
        self.application.config["MAIL_PASSWORD"] = os.environ.get("MAIL_PASSWORD")
        self.application.config["MAIL_USE_TLS"] = False
        self.application.config["MAIL_USE_SSL"] = True

        # Initialize MySQL credentials from the environment variables we just loaded.
        DB_HOST = os.environ.get("DB_HOST")
        DB_PORT = int(os.environ.get("DB_PORT"))
        DB_USER = os.environ.get("DB_USER")
        DB_PASSWORD = os.environ.get("DB_PASSWORD")
        DB_DB = os.environ.get("DB_DB") # database to use.
        # Set up SQLAlchemy with the above credentials.
        self.application.config["SQLALCHEMY_DATABASE_URI"] = f"mysql+pymysql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_DB}"
        # Set up an SQLAlchemy session for our application.
        db = sa(self.application)
        # creates Mail instance for managing emails
        mail = Mail(self.application)


        # Load environment variables from .env file.
        load_dotenv()

    def signup(self, client: FlaskClient, email: str, password: str):
        # sign up with given credentials 
        response: Response = client.post(
                '/register', data={'email': email, 'password': password}, follow_redirects=True)

        # Used to scrape signup data off the internet 
        soup = BeautifulSoup(response.data, 'html.parser')

        # Ensure that the log in page is showing
        self.assertIn('Log In', soup.find('title').text)

    def login(self, client: FlaskClient, email: str, password: str):
        # Log in with given credentials
        response: Response = client.post(
            '/login', data={'email': email, 'password': password}, follow_redirects=True
        )
        # Used to scrape signup data off the internet 
        soup = BeautifulSoup(response.data, 'html.parser')

        # Initialize MySQL credentials from the environment variables we just loaded.
        DB_HOST = os.environ.get("DB_HOST")
        DB_PORT = int(os.environ.get("DB_PORT"))
        DB_USER = os.environ.get("DB_USER")
        DB_PASSWORD = os.environ.get("DB_PASSWORD")
        DB_DB = os.environ.get("DB_DB") # database to use.
        # Set up SQLAlchemy with the above credentials.
        self.application.config["SQLALCHEMY_DATABASE_URI"] = f"mysql+pymysql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_DB}"
        # Set up an SQLAlchemy session for our application.
        db = sa(self.application)


        # Make sure login succeeded and the authorized link is showing
        self.assertTrue(soup.select('a[href="/auth/logout"]'))

class TestAuth(flask_unittest.AppClientTestCase):
    pass
    
    


    def test_user(self):
        # Assign the flask app 
        app = self.create_app()

if __name__ == '__main__':
    unittest.main()