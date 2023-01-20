from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, EmailField
from wtforms.validators import InputRequired, EqualTo, Length

class SignUpForm(FlaskForm):
    email = EmailField("Email:", validators=[
                          InputRequired(),Length(max=100)], render_kw={"placeholder": "EMAIL"})
    password = PasswordField("Password:", validators=[InputRequired(),Length(max=100)], render_kw={
                             "placeholder": "PASSWORD"})
    password2 = PasswordField("Confirm password:", validators=[InputRequired(), EqualTo("password"),Length(max=100)], render_kw={
        "placeholder": "CONFIRM PASSWORD"})
    submit = SubmitField("REGISTER")