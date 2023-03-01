from flask import Blueprint, g, render_template, url_for, redirect
from application.modules.auth import login_required, team_required
from application.data_models import *
from application.forms import *
from wtforms.validators import ValidationError

deals_bp = Blueprint('deals_bp', __name__, template_folder="templates")

@deals_bp.route("/deals", defaults={"filter": "all", "page": 1, "prev_sort": "None", "sort": "None", "order": "DESC", "error": "None"}, methods=["GET", "POST"])
@deals_bp.route("/deals/<filter>/<prev_sort>/<sort>/<page>/<order>/<error>", methods=["GET", "POST"])
@login_required
@team_required
def deals(filter, page, error, prev_sort, sort, order):
    
    # Search bar.
    search_form = DealsSearchForm()
    #deals = None
    deals = Deals.query
    
    # Gets all contacts of user that is logged in and passes it to html template
    user = Users.query.filter_by(email=g.email).first()
    deals = Deals.query.filter_by(team_id=user.team_id)


    # Filters contact results
    if filter == "assigned":
        deals = Deals.query.filter_by(
            team_id=user.team_id, owner=user.email)
    elif filter == "unassigned":
        deals = Deals.query.filter_by(
            team_id=user.team_id, owner="")
    else:
        deals = Deals.query.filter_by(team_id=user.team_id)

    if search_form.validate_on_submit():
        user_search = search_form.search_bar.data
        # Before using the user's search let's optimize for it.
        optimization = optimize_deals_search(user_search)
        # If the user is looking for an name, only search the name column.
        if optimization == "name":
            deals = deals.filter(Deals.name.like(f"%{user_search}%"))
        # If the user is looking for an number, only search the number column.
        elif optimization == "deal_id":
            deals = deals.filter(Deals.deal_id.like(f"%{user_search}%"))
        # If the user is looking for an email, only search the email column.
        elif optimization == "associated_contact":
            deals = deals.filter(Deals.associated_contact.like(f"%{user_search}%"))
        # If the user isn't looking for an email or number definitively then search all relevant columns.
        else:
            deals = deals.filter(Deals.associated_contact.like(f"%{user_search}%") | Deals.name.like(f"%{user_search}%") | Deals.deal_id.like(f"%{user_search}%"))
 
                  
    # Add deal form.
    add_deal = DealForm()
    # The page the user wishes to view.
    page = int(page)
    # Must offset results from DB query to fetch the page the user is interested in.
    page_offset = (page - 1) * 25
    '''
    # Gets all contacts of user that is logged in and passes it to html template
    user = Users.query.filter_by(email=g.email).first()
    deals = Deals.query.filter_by(team_id=user.team_id)
    '''
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
        deals = order_deals(sort, order, deals)
    
    # Pageing functionality.
    deals = deals.limit(25).offset(page_offset)
    num_pages = deals.count() // 25


    # Count the number of pages.
    if (deals.count() % 25) > 0:
        num_pages += 1

    
    # Create an editable form for each contact. Will only ever 25 at a time.
    forms = []
    for deal in deals:
        form = DealForm()
        
        form.deal_id.data = deal.deal_id
        form.name.data = deal.name
        form.stage.data = deal.stage
        form.date.data = deal.close_date
        form.owner.data = deal.owner
        form.amount.data = deal.amount
        form.goal.data = deal.goal
        form.associated_contact.data = deal.associated_contact
        form.associated_company.data = deal.associated_company
        forms.append(form)
        
    return render_template("deals.html", forms=forms, add_deal=add_deal, num_pages=num_pages, page=page, error=error, search_form=search_form, filter=filter, prev_sort=prev_sort, sort=sort, order=order)

    
def optimize_deals_search(search):
        """Report back to the caller whether the search term is likely an email or otherwise."""
        if "@" in search and "." in search:
            return "email"
        else:
            return "name/company/email"

def order_deals(sort, order, deals):
    """Sort the results of a Deals query based on the sort (column name) and order (ASC/DESC) paramaters."""
    if sort == "name":
        if order == "ASC":
            deals = deals.order_by(Deals.name)
        else:
            deals = deals.order_by(Deals.name.desc())
    
    elif sort == "associated_contact":
        if order == "ASC":
            deals = deals.order_by(Deals.associated_contact)
        else:
            deals = deals.order_by(Deals.associated_contact.desc())
    
    elif sort == "associated_company":
        if order == "ASC":
            deals = deals.order_by(Deals.associated_company)
        else:
            deals = deals.order_by(Deals.associated_company.desc())

    elif sort == "amount":
        if order == "ASC":
            deals = deals.order_by(Deals.amount)
        else:
            deals = deals.order_by(Deals.amount.desc())

    elif sort == "owner":
        if order == "ASC":
            deals = deals.order_by(Deals.owner)
        else:
            deals = deals.order_by(Deals.owner.desc())

    elif sort == "stage" :
        if order == "ASC":
            deals = deals.order_by(Deals.stage)
        else:
            deals = deals.order_by(Deals.stage.desc())

    else :
        if order == "ASC":
            deals = deals.order_by(Deals.close_date)
        else:
            deals = deals.order_by(Deals.close_date.desc())
    print(sort)
    return deals

@deals_bp.route("/add_deal", defaults={"filter": "all", "page": 1, "prev_sort": "None", "sort": "None", "order": "DESC", "error": "None"}, methods=["GET", "POST"])
@deals_bp.route("/add_deal/<filter>/<prev_sort>/<sort>/<page>/<order>/<error>", methods=["GET", "POST"])
@login_required
@team_required
def add_deal(filter, page, error, prev_sort, sort, order):
    form = DealForm()
    user = Users.query.filter_by(email=g.email).first()
    deals = Deals.query.filter_by(team_id=user.team_id)
    error = "None"
    
    deal = Deals()
    deal.team_id = user.team_id
    deal.name = form.name.data
    deal.stage = dict(form.stage.choices).get(form.stage.data)
    deal.close_date = form.date.data
    deal.owner = form.owner.data 
    deal.amount = form.amount.data 
    deal.associated_contact = form.associated_contact.data
    deal.associated_company = form.associated_company.data

    db.session.add(deal)     
    db.session.commit()

    if form.owner.data != "" and Users.query.filter_by(email=form.owner.data, team_id=user.team_id).first() is None:
                error = "Invalid deal owner"

    #return redirect(url_for("deals_bp.deals", page=page, error=error))
    return redirect(url_for("deals_bp.deals", page=page, filter="all", prev_sort="None", sort="None", order="DESC", error=error))
    #return redirect(url_for("deals_bp.deals",prev_sort=prev_sort, order=order, sort=sort, filter=filter, page=page, error=error))


@deals_bp.route("/edit_deal", defaults={"deal_id": "None", "page": 1, "error": "None"}, methods=["GET", "POST"])
@deals_bp.route("/edit_deal/<deal_id>/<page>/<error>", methods=["GET", "POST"])
@login_required
@team_required
def edit_deal(deal_id, page, error):
    form = DealForm()
    deal = Deals.query.filter_by(deal_id=deal_id).first()       
    if deal is not None:
        user = Users.query.filter_by(email=g.email).first()
        
    if "Closed" in form.stage.data:
        if form.amount.data == "":
            error = "Close Amount must be inputted when closing an amount"
        elif int(form.amount.data) == 0:
            error = "Close Amount must be inputted when closing an amount"
        elif form.date.data == None:
            error = "Close Date must be inputted when closing a deal"
       
    if error == "None":
        deal = Deals()
        deal.team_id = user.team_id
        deal.name = form.name.data
        deal.stage = dict(form.stage.choices).get(form.stage.data)
        deal.close_date = form.date.data
        deal.owner = form.owner.data 
        deal.amount = form.amount.data 
        deal.goal = form.goal.data
        deal.associated_contact = form.associated_contact.data
        deal.associated_company = form.associated_company.data
        db.session.add(deal)     
        db.session.commit()

    if form.owner.data != "" and Users.query.filter_by(email=form.owner.data, team_id=user.team_id).first() is None:
                error = "Invalid deal owner"

    #return redirect(url_for("deals_bp.deals", page=page, error=error))
    return redirect(url_for("deals_bp.deals", page=page, filter="all", prev_sort="None", sort="None", order="DESC", error=error))
    #return redirect(url_for("deals_bp.deals",prev_sort=prev_sort, order=order, sort=sort, filter=filter, page=page, error=error))
