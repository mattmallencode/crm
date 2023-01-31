from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, EmailField, SelectField, BooleanField
from wtforms.validators import InputRequired, EqualTo, Email, Length

class SignUpForm(FlaskForm):
    name = StringField("Name", validators=[InputRequired()], render_kw={"placeholder": "FULL NAME"})
    email = EmailField("Email:", 
        validators=[InputRequired(), Email(), Length(max=100)], render_kw={"placeholder": "EMAIL"})
    password = PasswordField("Password:", 
        validators=[InputRequired(),Length(max=100)], render_kw={"placeholder": "PASSWORD"})
    password2 = PasswordField("Confirm password:", 
        validators=[InputRequired(), EqualTo("password"),Length(max=100)], render_kw={"placeholder": "CONFIRM PASSWORD"})
    submit = SubmitField("REGISTER")

class LoginForm(FlaskForm):
    email = StringField("EMAIL:", 
        validators=[InputRequired(), Length(max=100)], render_kw={"placeholder": "EMAIL"})
    password = PasswordField("Password:", 
        validators=[InputRequired(),Length(max=100)], render_kw={"placeholder": "PASSWORD"})

    submit = SubmitField("LOGIN")

class CreateTeamForm(FlaskForm):
    name = StringField("Team Name:", validators=[InputRequired()])
    submit = SubmitField("Create Team")

class InviteForm(FlaskForm):
    email = EmailField("Email:", validators=[InputRequired(), Email()])
    submit = SubmitField("Send Invitation")

class ContactForm(FlaskForm):
    name = StringField("Name", validators=[InputRequired()])
    email = EmailField("Email", validators=[InputRequired(), Email()])
    phone_number = StringField("Phone Number")
    contact_owner = StringField("Contact Owner", validators=[Email()])
    company = StringField("Company")
    status = SelectField("Status", choices = [("New", "New"), ("Open", "Open"), ("In Progress", "In Progress"), ("Open Deal", "Open Deal"), ("Unqualified", "Unqualified"), ("Attempted To Contact", "Attempted To Contact"), ("Connected", "Connected"), ("Bad Timing", "Bad Timing")])
    submit = SubmitField("Add Contact")

class removeContactForm(FlaskForm):
    email = EmailField("Email", validators=[InputRequired(), Email()])
    submit = SubmitField("Remove Contact")

class LogoutForm(FlaskForm):
    submit = SubmitField("Log Out")

class LeaveTeamForm(FlaskForm):
    sure_checkbox = BooleanField("Please click to confirm leaving your team.")
    submit = SubmitField("Leave Team")

class SearchForm(FlaskForm):
    search_bar = StringField("Search Contacts...")
    submit = SubmitField("Search")