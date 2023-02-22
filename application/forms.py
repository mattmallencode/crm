from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, EmailField, SelectField, BooleanField, DateTimeField, DateTimeLocalField
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
    contact_id = StringField()
    name = StringField("Name", validators=[InputRequired()])
    email = EmailField("Email", validators=[InputRequired(), Email()])
    phone_number = StringField("Phone Number")
    contact_owner = StringField("Contact Owner")
    company = StringField("Company")
    status = SelectField("Status", choices = [("New", "New"), ("Open", "Open"), ("In Progress", "In Progress"), ("Open Deal", "Open Deal"), ("Unqualified", "Unqualified"), ("Attempted To Contact", "Attempted To Contact"), ("Connected", "Connected"), ("Bad Timing", "Bad Timing")])
    submit = SubmitField("")

class EmailForm(FlaskForm):
    subject = StringField("Subject")
    message = StringField("Message")
    submit = SubmitField("Send")

class MeetingForm(FlaskForm):
    title = StringField("Title")
    description = StringField("Description")
    date_time_start = DateTimeField("Start: ", render_kw={"type": "datetime-local"}, validators=[InputRequired()], format="%Y-%m-%dT%H:%M")
    date_time_end = DateTimeField("End: ", render_kw={"type": "datetime-local"}, validators=[InputRequired()], format="%Y-%m-%dT%H:%M")
    schedule = SubmitField("Schedule")

class removeContactForm(FlaskForm):
    email = EmailField("Email", validators=[InputRequired(), Email()])
    submit = SubmitField("Remove Contact")

class LogoutForm(FlaskForm):
    submit = SubmitField("Log Out")

class LeaveTeamForm(FlaskForm):
    sure_checkbox = BooleanField("Click the checkbox to confirm you are leaving your team")
    submit = SubmitField("Leave Team")

class SearchForm(FlaskForm):
    search_bar = StringField("Search...")
    submit = SubmitField("Search")

class NoteForm(FlaskForm):
    note = StringField("Note", validators=[Length(1, 140, "Note must be between 1 and 140 characters in length")])
    submit = SubmitField("Add Note")

class DealForm(FlaskForm):
    deal_id = StringField()
    name = StringField("Deal Name", validators=[InputRequired()])
    stage = SelectField("Deal Stage", choices=[("Appointment Scheduled", "Appointment Scheduled"), 
    ("Qualified To Buy", "Qualified To Buy"), ("Presentation Scheduled", "Presentation Scheduled"), 
    ("Decision Maker Brought-In", "Decision Maker Brought-In"), ("Contract Sent", "Contract Sent"), 
    ("Closed Won", "Closed Won"), ("Closed Lost", "Closed Lost")])
    date = DateTimeLocalField("Close Date",format='%Y-%m-%dT%H:%M')
    owner = StringField("Deal Owner")
    amount = StringField("Amount")
    associated_contact = StringField("Associated Contact")
    associated_company = StringField("Associated Company")
    submit = SubmitField()

class DealsSearchForm(FlaskForm):
    search_bar = StringField("Search Deals...")
    submit = SubmitField("Search")


