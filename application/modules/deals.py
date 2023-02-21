from flask import Blueprint, g, render_template, url_for, redirect
from application.modules.auth import login_required, team_required
from application.data_models import *
from application.forms import *

deals_bp = Blueprint('deals_bp', __name__, template_folder="templates")

@deals_bp.route("/deals", defaults={"page": 1, "error": "None"}, methods=["GET", "POST"])
@deals_bp.route("/deals/<page>/<error>", methods=["GET", "POST"])
@login_required
@team_required
def deals(page, error):
    # Add deal form.
    add_deal = DealForm()
    # The page the user wishes to view.
    page = int(page)
    # Must offset results from DB query to fetch the page the user is interested in.
    page_offset = (page - 1) * 25

    # Gets all contacts of user that is logged in and passes it to html template
    user = Users.query.filter_by(email=g.email).first()
    deals = Deals.query.filter_by(team_id=user.team_id)

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
        form.associated_contact.data = deal.associated_contact
        form.associated_company.data = deal.associated_company
        forms.append(form)

    return render_template("deals.html", forms=forms, add_deal=add_deal, num_pages=num_pages, page=page, error=error)



@deals_bp.route("/add_deal", defaults={"page": 1, "error": "None"}, methods=["GET", "POST"])
@deals_bp.route("/add_deal/<page>/<error>", methods=["GET", "POST"])
@login_required
@team_required
def add_deal(page, error):
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

    return redirect(url_for("deals_bp.deals", page=page, error=error))


@deals_bp.route("/edit_deal", defaults={"deal_id": "None", "page": 1, "error": "None"}, methods=["GET", "POST"])
@deals_bp.route("/edit_deal/<deal_id>/<page>/<error>", methods=["GET", "POST"])
@login_required
@team_required
def edit_deal(deal_id, page, error):
    form = DealForm()
    deal = Deals.query.filter_by(deal_id=deal_id).first()       
    if deal is not None:
        user = Users.query.filter_by(email=g.email).first()
        
        deal.team_id = user.team_id
        deal.name = form.name.data
        deal.stage = dict(form.stage.choices).get(form.stage.data)
        deal.close_date = form.date.data
        deal.owner = form.owner.data 
        deal.amount = form.amount.data 
        deal.associated_contact = form.associated_contact.data
        deal.associated_company = form.associated_company.data

        print(form.date.data)

        db.session.commit()
    return redirect(url_for("deals_bp.deals", page=page, error=error))