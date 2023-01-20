from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, DecimalField, IntegerField, EmailField

class SignUpForm(FlaskForm):
    email = EmailField()
    password = PasswordField