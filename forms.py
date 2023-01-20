from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, EmailField
from wtforms.validators import InputRequired, EqualTo

class SignUpForm(FlaskForm):
    email = EmailField("Email:", validators=[
                          InputRequired()], render_kw={"placeholder": "EMAIL"})
    password = PasswordField("Password:", validators=[InputRequired()], render_kw={
                             "placeholder": "PASSWORD"})
    password2 = PasswordField("Confirm password:", validators=[InputRequired(), EqualTo("password")], render_kw={
        "placeholder": "CONFIRM PASSWORD"})
    submit = SubmitField("REGISTER")