from flask import Blueprint, g, render_template, current_app, redirect, url_for
import re
from application.modules.auth import login_required, team_required
from application.forms import SearchForm, ContactForm, LogoutForm
from application.data_models import *

contacts_bp = Blueprint('contacts_bp', __name__, template_folder="templates")
turbo = current_app.extensions.get("turbo")

@contacts_bp.route("/contacts", defaults={"filter": "all", "page": 1, "prev_sort": "None", "sort": "None", "order": "DESC", "error": "None"}, methods=["GET", "POST"])
@contacts_bp.route("/contacts/<filter>/<prev_sort>/<sort>/<page>/<order>/<error>", methods=["GET", "POST"])
@login_required
@team_required
def contacts(filter, page, prev_sort, sort, order, error):
    """
    Displays list of contacts registered with this team.

    filter -- whether to show all contacts, assigned contatcs, or uanssigned contacts.
    prev_sort -- the last way the contacts were sorted e.g. NameASC (if any).
    sort -- the current way the contacts are being sorted e.g. NameDESC (if any).
    page -- the page of contacts the user wishes to view (25 contacts per page).
    order -- the order of the sort (if any), must be ASC or DESC.
    error -- error message due to form invalidation.
    """

    # Search bar.
    search_form = SearchForm()
    # Add contact form.
    add_contact = ContactForm()
    logout_form = LogoutForm()
    # The page the user wishes to view.
    page = int(page)
    # Must offset results from DB query to fetch the page the user is interested in.
    page_offset = (page - 1) * 25

    # Gets all contacts of user that is logged in and passes it to html template
    user = Users.query.filter_by(email=g.email).first()

    # Filters contact results
    if filter == "assigned":
        contacts = Contacts.query.filter_by(
            team_id=user.team_id, contact_owner=user.email)
    elif filter == "unassigned":
        contacts = Contacts.query.filter_by(
            team_id=user.team_id, contact_owner="")
    else:
        contacts = Contacts.query.filter_by(team_id=user.team_id)

    if search_form.validate_on_submit():
        user_search = search_form.search_bar.data
        # Before using the user's search let's optimize for it.
        optimization = optimize_search(user_search)
        # If the user is looking for an email, only search the email column.
        if optimization == "email":
            contacts = contacts.filter(Contacts.email.like(f"%{user_search}%"))
        # If the user is looking for an number, only search the number column.
        elif optimization == "number":
            contacts = contacts.filter(
                Contacts.phone_number.like(f"%{user_search}%"))
        # If the user isn't looking for an email or number definitively then search all relevant columns.
        else:
            contacts = contacts.filter(Contacts.email.like(f"%{user_search}%") | Contacts.name.like(
                f"%{user_search}%") | Contacts.company.like(f"%{user_search}%"))
    # Toggle feature of sort buttons, if the user is sorting a different column to last sort, order is ascending.
    if sort != prev_sort:
        order = "ASC"
    else:
        # User is toggling a sort they already did e.g. their second or third time clicking to sort name.
        if order == "ASC":
            order = "DESC"
        else:
            order = "ASC"
    # Only sort if the user asks us to.
    if sort != "None":
        contacts = order_contacts(sort, order, contacts)
    num_pages = contacts.count() // 25

    # Count the number of pages.
    if (contacts.count() % 25) > 0:
        num_pages += 1

    # Create an editable form for each contact. Will only ever 25 at a time.
    forms = []
    for contact in contacts:
        form = ContactForm()
        form.contact_id.data = contact.contact_id
        form.name.data = contact.name
        form.email.data = contact.email
        form.phone_number.data = contact.phone_number
        form.contact_owner.data = contact.contact_owner
        form.company.data = contact.company
        form.status.data = contact.status
        forms.append(form)
        
    return render_template("contacts.html", forms=forms, add_contact=add_contact, search_form=search_form, contacts=contacts, num_pages=num_pages, filter=filter, page=page, prev_sort=prev_sort, sort=sort, order=order, error=error, activity="editing")


def optimize_search(search):
    """Report back to the caller whether the search term is likely an email, number, or otherwise."""
    if "@" in search or "." in search:
        return "email"
    if re.search('[a-zA-Z]', search) == None:
        return "number"
    else:
        return "name/company/email"


def order_contacts(sort, order, contacts):
    """Sort the results of a contacts query based on the sort (column name) and order (ASC/DESC) paramaters."""
    if sort == "name":
        if order == "ASC":
            contacts = contacts.order_by(Contacts.name)
        else:
            contacts = contacts.order_by(Contacts.name.desc())
    elif sort == "email":
        if order == "ASC":
            contacts = contacts.order_by(Contacts.email)
        else:
            contacts = contacts.order_by(Contacts.email.desc())
    elif sort == "phone_number":
        if order == "ASC":
            contacts = contacts.order_by(Contacts.phone_number)
        else:
            contacts = contacts.order_by(Contacts.phone_number.desc())
    elif sort == "contact_owner":
        if order == "ASC":
            contacts = contacts.order_by(Contacts.contact_owner)
        else:
            contacts = contacts.order_by(Contacts.contact_owner.desc())
    elif sort == "company":
        if order == "ASC":
            contacts = contacts.order_by(Contacts.company)
        else:
            contacts = contacts.order_by(Contacts.company.desc())
    elif sort == "status":
        if order == "ASC":
            contacts = contacts.order_by(Contacts.status)
        else:
            contacts = contacts.order_by(Contacts.status.desc())
    return contacts




@contacts_bp.route("/add_contact", defaults={"filter": "all", "page": 1, "prev_sort": "None", "sort": "None", "order": "DESC", "error": "None"}, methods=["GET", "POST"])
@contacts_bp.route("/add_contact/<filter>/<prev_sort>/<sort>/<page>/<order>/<error>", methods=["GET", "POST"])
@login_required
@team_required
def add_contact(filter, page, prev_sort, sort, order, error):
    """
    Add a new contact to this team.
    filter -- whether to show all contacts, assigned contatcs, or uanssigned contacts.
    prev_sort -- the last way the contacts were sorted e.g. NameASC (if any).
    sort -- the current way the contacts are being sorted e.g. NameDESC (if any).
    page -- the page of contacts the user wishes to view (25 contacts per page).
    order -- the order of the sort (if any), must be ASC or DESC.
    error -- error message due to form invalidation.
    """
    form = ContactForm()
    user = Users.query.filter_by(email=g.email).first()
    user_contacts = Contacts.query.filter_by(team_id=user.team_id)
    error = "None"
    if form.validate_on_submit():
        #  checks if contact being added belongs to user's organization already
        if Contacts.query.filter_by(email=form.email.data, team_id=user.team_id).first() is None:
            team_id = user.team_id

            contact = Contacts()
            contact.contact_id = f"{form.email.data}_{team_id}"
            contact.team_id = team_id
            contact.name = form.name.data
            contact.email = form.email.data
            contact.phone_number = form.phone_number.data
            # If the user's included a contact owner, check that the contact owner is a member of the organisation.
            if form.contact_owner.data != "" and Users.query.filter_by(email=form.contact_owner.data, team_id=user.team_id).first() is None:
                error = "Invalid contact owner email"
            else:
                # If the user's isn't editing the contact save changes, otherwise check that they're an admin.
                if contact.contact_owner == "" or user.admin_status == True:
                    contact.contact_owner = form.contact_owner.data

                    contact.company = form.company.data
                    contact.status = dict(
                        form.status.choices).get(form.status.data)

                    db.session.add(contact)
                    db.session.commit()
                else:
                    error = "You do not have sufficient permissions to assign a contact."
        else:
            error = "This person is already in your contacts"
    return redirect(url_for("contacts_bp.contacts", prev_sort=prev_sort, order=order, sort=sort, page=page, filter=filter, error=error))

@contacts_bp.route("/remove_contact/<contact_id>/<filter>/<prev_sort>/<sort>/<page>/<order>/<error>", methods=["GET", "POST"])
@login_required
@team_required
def remove_contact(contact_id, filter, page, prev_sort, sort, order, error):
    """
    Retrieves contact specified in parameter and removes from Contacts table.
    contact_id -- contact to be removed.
    filter -- whether to show all contacts, assigned contatcs, or uanssigned contacts.
    prev_sort -- the last way the contacts were sorted e.g. NameASC (if any).
    sort -- the current way the contacts are being sorted e.g. NameDESC (if any).
    page -- the page of contacts the user wishes to view (25 contacts per page).
    order -- the order of the sort (if any), must be ASC or DESC.
    error -- error message due to form invalidation.
    """
    contact = Contacts.query.filter_by(contact_id=contact_id).first()
    if contact is not None:
        db.session.delete(contact)
        db.session.commit()
    return redirect(url_for("contacts_bp.contacts", prev_sort=prev_sort, order=order, sort=sort, page=page, filter=filter, error=error))
    


@contacts_bp.route("/edit_contact", defaults={"contact_id": "None", "filter": "all", "page": 1, "prev_sort": "None", "sort": "None", "order": "DESC", "error": "None"}, methods=["GET", "POST"])
@contacts_bp.route("/edit_contact/<contact_id>/<filter>/<prev_sort>/<sort>/<page>/<order>/<error>", methods=["GET", "POST"])
@login_required
@team_required
def edit_contact(contact_id, filter, page, prev_sort, sort, order, error):
    """
    Edit an existing contact in the database.
    contact_id -- contact being edited.
    filter -- whether to show all contacts, assigned contatcs, or uanssigned contacts.
    prev_sort -- the last way the contacts were sorted e.g. NameASC (if any).
    sort -- the current way the contacts are being sorted e.g. NameDESC (if any).
    page -- the page of contacts the user wishes to view (25 contacts per page).
    order -- the order of the sort (if any), must be ASC or DESC.
    error -- error message due to form invalidation.
    """
    form = ContactForm()
    error = "None"
    if form.validate_on_submit():
        user = Users.query.filter_by(email=g.email).first()
        contact = Contacts.query.filter_by(
            contact_id=contact_id, team_id=g.team_id).first()
        contact.name = form.name.data
        contact.email = form.email.data
        former_id = contact.contact_id
        contact.contact_id = f"{form.email.data}_{contact.team_id}"
        dupe_contact = None
        # If the user is editing the email of the user their contact_id will change.
        # We need to make sure they're not making a duplicate contact_id.
        if contact.contact_id != former_id:
            # If the contact_id does not already exist, this query will work and return none.
            try:
                dupe_contact = Contacts.query.filter_by(
                    contact_id=contact.contact_id).first()
            # If the contact_id already exists, this query throws an exception and we can set dupe_contact manually.s
            except:
                dupe_contact = "Duplicate!"
        # If the user isn't trying to create a duplicate contact.
        if dupe_contact == None:
            contact.phone_number = form.phone_number.data
            # If the user's editing the contact owner data, make sure they're assigning it to a valid member of their team.
            if form.contact_owner.data != "" and Users.query.filter_by(email=form.contact_owner.data, team_id=user.team_id).first() is None:
                error = "Invalid User Email"
            else:
                # If the user's isn't editing the contact save changes, otherwise check that they're an admin.
                if form.contact_owner.data == contact.contact_owner or user.admin_status == True:
                    contact.contact_owner = form.contact_owner.data
                    contact.company = form.company.data
                    contact.status = dict(
                        form.status.choices).get(form.status.data)
                    db.session.flush()
                    db.session.refresh(contact)
                    contact.contact_id = f"{form.email.data}_{g.team_id}"
                    db.session.flush()
                    db.session.commit()
                else:
                    error = "You do not have sufficient permissions to assign a contact."
        else:
            error = "Can't create a duplicate contact!"
    return redirect(url_for('contacts_bp.contacts', prev_sort=prev_sort, order=order, sort=sort, page=page, filter=filter, error=error))