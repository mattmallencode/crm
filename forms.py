from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, EmailField, SelectField
from wtforms.validators import InputRequired, EqualTo, Email, Length

class SignUpForm(FlaskForm):
    email = EmailField("Email:", 
        validators=[InputRequired(), Email(), Length(max=100)], render_kw={"placeholder": "EMAIL"})
    password = PasswordField("Password:", 
        validators=[InputRequired(),Length(max=100)], render_kw={"placeholder": "PASSWORD"})
    password2 = PasswordField("Confirm password:", 
        validators=[InputRequired(), EqualTo("password"),Length(max=100)], render_kw={"placeholder": "CONFIRM PASSWORD"})
    submit = SubmitField("REGISTER")

class LoginForm(FlaskForm):
    email = StringField("EMAIL:", 
        validators=[InputRequired(), Length(max=100)], render_kw={"placeholder": "USERNAME"})
    password = PasswordField("Password:", 
        validators=[InputRequired(),Length(max=100)], render_kw={"placeholder": "PASSWORD"})

    submit = SubmitField("LOGIN")

class CreateTeamForm(FlaskForm):
    team_id = StringField("Team id:", 
        validators=[InputRequired(), Email(), Length(min=10, max=100)], render_kw={"placeholder": "EMAIL"})
    password = PasswordField("Password:", 
        validators=[InputRequired(),Length(max=100)], render_kw={"placeholder": "PASSWORD"})
    password2 = PasswordField("Confirm password:", 
        validators=[InputRequired(), EqualTo("password"),Length(max=100)], render_kw={"placeholder": "CONFIRM PASSWORD"})
    submit = SubmitField("REGISTER")

class InviteForm(FlaskForm):
    email = EmailField("Email:", validators=[InputRequired(), Email()])
    submit = SubmitField("Send Invitation")

class addContactForm(FlaskForm):
    name = StringField("Name", validators=[InputRequired()])
    email = EmailField("Email", validators=[InputRequired(), Email()])
    phone_number = StringField("Phone Number")
    contact_owner = StringField("Contact Owner")
    company = StringField("Company")
    status = SelectField("Status", choices = [("new", "New"), ("open", "Open"), ("progress", "In Progress"), ("deal", "Open Deal"), ("unqualified", "Unqualified"), ("attempt", "Attempted To Contact"), ("connected", "Connected"), ("timing", "Bad Timing")])
    submit = SubmitField("Add Contact")


