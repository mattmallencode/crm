from flask import current_app

db = current_app.extensions.get("sqlalchemy")

# Users data model i.e. a representation of the users table in the database.


class Users(db.Model):
    email = db.Column(db.String, primary_key=True)
    password_hash = db.Column(db.String)
    team_id = db.Column(db.Integer)
    owner_status = db.Column(db.Boolean)
    admin_status = db.Column(db.Boolean)
    name = db.Column(db.String)

    def __init__(self, email=None, password_hash=None, team_id=None, owner_status=None, admin_status=None, name=None):
        self.email = email
        self.password_hash = password_hash
        self.team_id = team_id
        self.owner_status = owner_status
        self.admin_status = admin_status
        self.name = name

# Invites data model i.e. a representation of the users table in the database.


class Invites(db.Model):
    invite_id = db.Column(db.String, primary_key=True)
    team_id = db.Column(db.Integer)

    def __init__(self, invite_id=None, team_id=None):
        self.invite_id = invite_id
        self.team_id = team_id

# Contacts data model i.e. a representation of the contacts table in the database.


class Contacts(db.Model):
    contact_id = db.Column(db.String, primary_key=True)
    team_id = db.Column(db.Integer)
    name = db.Column(db.String)
    email = db.Column(db.String)
    phone_number = db.Column(db.Integer)
    contact_owner = db.Column(db.String)
    company = db.Column(db.String)
    status = db.Column(db.String)

    def __init__(self, contact_id=None, team_id=None, name=None, email=None, phone_number=None, contact_owner=None, company=None, status=None):
        self.contact_id = contact_id
        self.team_id = team_id
        self.name = name
        self.email = email
        self.phone_number = phone_number
        self.contact_owner = contact_owner
        self.company = company
        self.status = status

# Teams data model i.e. a representation of the teams table in the database.


class Teams(db.Model):
    team_id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String)

    def __init__(self, team_id=None, name=None):
        self.team_id = team_id
        self.name = name


class Notes(db.Model):
    note_id = db.Column(db.Integer, primary_key=True)
    contact_id = db.Column(db.String)
    note = db.Column(db.String)
    author = db.Column(db.String)
    date = db.Column(db.String)

    def __init__(self, note_id=None, contact_id=None, note=None, author=None, date=None):
        self.note_id = note_id
        self.contact_id = contact_id
        self.note = note
        self.author = author
        self.date = date


# Deals data model i.e. a representation of the deals table in the database.

class Deals(db.Model):
    deal_id = db.Column(db.Integer, primary_key=True)
    team_id = db.Column(db.Integer)
    name = db.Column(db.String)
    stage = db.Column(db.String)
    close_date = db.Column(db.DateTime)
    owner = db.Column(db.String)
    amount = db.Column(db.Integer)
    goal = db.Column(db.Integer)
    associated_contact = db.Column(db.String)
    associated_company = db.Column(db.String)

    def __init__ (self, deal_id=None, team_id=None, name=None, stage=None, close_date=None, owner=None, amount=None, goal=None, associated_contact=None, associated_company=None):
        self.deal_id = deal_id
        self.team_id = team_id
        self.name = name
        self.stage = stage
        self.close_date = close_date
        self.owner = owner
        self.amount = amount
        self.goal = goal
        self.associated_contact = associated_contact
        self.associated_company = associated_company
