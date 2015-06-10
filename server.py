"""GlowBB"""

from jinja2 import StrictUndefined
from flask import Flask, jsonify, render_template, redirect, request, flash, session
# from flask_debugtoolbar import DebugToolbarExtension
from model import connect_to_db, db, User, User_Concern, Concern, Beauty_Type, Product_Category, Product, Rating
import praw, datetime, os, nltk
import operator
from operator import itemgetter
from sqlalchemy import or_
# from lib.helpers import hash
# import json

app = Flask(__name__)

# Required to use Flask sessions and the debug toolbar
app.secret_key = "ABC"
# app.debug = True

# Normally, if you use an undefined variable in Jinja2, it fails silently.
# This is horrible. Fix this so that, instead, it raises an error.
app.jinja_env.undefined = StrictUndefined


@app.route('/')
def index():
    """Homepage."""

    return render_template('homepage.html')


@app.route('/register', methods=['GET'])
def register_form():
    """Show form for user signup."""

    return render_template("register_form.html")


@app.route('/register', methods=['POST'])
def register_process():
    """Process registration."""

    # Get registration form variables
    email = request.form["email"]
    password = request.form["password"]
    firstname = request.form["firstname"]
    lastname = request.form["lastname"]
    zipcode = request.form["zipcode"]

    new_user = User(email=email, password=password, firstname=firstname, lastname=lastname, zipcode=zipcode)

    # Adds the new user to the database. Session of connection to DB.
    db.session.add(new_user)
    db.session.commit()

    #browser/cookie storing session
    session["user_id"] = new_user.user_id

    flash("User %s added." % email)

    # Takes user to profile form immediately after submitting registration.
    return redirect("/profile")


@app.route('/login', methods=['GET'])
def login_form():
    """Show form for user login"""

    return render_template("login_form.html")


@app.route('/login', methods=['POST'])
def login_process():
    """Process login"""

    email = request.form["email"]
    password = request.form["password"]

    user = User.query.filter_by(email=email).first()

    if not user:
        flash("User does not exist. Please try again")
        return redirect("/login")

    if user.password != password:
        flash("Password is not correct. Please try again.")
        return redirect("/login")

    session["user_id"] = user.user_id

    flash("You are logged in!")

    # Takes the user to their user page when they login.
    return redirect("/users/%s" % user.user_id)


@app.route('/logout')
def logout():
    """Logs user out, redirects to Homepage"""

    del session["user_id"]
    flash("You have logged out.")
    return redirect("/")


@app.route('/profile', methods=['GET'])
def profile_form():
    """Show form for user profile."""

    user_id = session.get("user_id")

    if not user_id:
        flash("User must be logged in.")
        return redirect("/login")

    return render_template("profile_form.html")


@app.route('/profile', methods=['POST'])
def profile_process():
    """Process profile form - assigning & returning user's Beauty Type"""

    user_id = session.get("user_id")

    if not user_id:
        flash("User does not exist. Please try again")
        return redirect("/login")

    user = User.query.get(user_id)

    # Gets profile form variables and adds them to user_id.
    #Q1 & 2: Gets user's skin type (both radio)
    skin_type = request.form.get("skin_type")
    skin_condition = request.form.get("skin_condition")

    #Q3: Allows user to select up to 3 skin "concerns" from list (checkbox)
    acne = request.form.get("acne")
    aging = request.form.get("aging")
    clogged = request.form.get("clogged")
    dryness = request.form.get("dryness")
    dullness = request.form.get("dullness")
    irritated = request.form.get("irritated")
    oiliness = request.form.get("oiliness")
    scars = request.form.get("scars")

#Dictionary of all beauty types w/values of 0. Values are incremented depending
#on how profile form questions are answered. Dictonary sorted backwards by value.
#Beauty type/key with highest value is assigned to user as their beauty type.
    beauty_types = {
        1: 0,  # starfish/oily
        2: 0,  # snail/combination
        3: 0,  # bee/normal
        4: 0,  # butterfly/dry
        5: 0, }  # dragonfly/dehydrated

    """STARFISH 1"""
    if skin_type and skin_condition == "Oily":
        beauty_types[1] += 50

    if acne == "true":
        beauty_types[1] += 0

    if aging == "true":
        beauty_types[1] += 0

    if clogged == "true":
        beauty_types[1] += 0

    if dryness == "true":
        beauty_types[1] += 0

    if dullness == "true":
        beauty_types[1] += 0

    if irritated == "true":
        beauty_types[1] += 0

    if oiliness == "true":
        beauty_types[1] += 0

    if scars == "true":
        beauty_types[1] += 0

    """SNAIL 2"""
    if skin_type and skin_condition == "Combination":
        beauty_types[2] += 50

    if acne == "true":
        beauty_types[2] += 0

    if aging == "true":
        beauty_types[2] += 0

    if clogged == "true":
        beauty_types[2] += 0

    if dryness == "true":
        beauty_types[2] += 0

    if dullness == "true":
        beauty_types[2] += 0

    if irritated == "true":
        beauty_types[2] += 0

    if oiliness == "true":
        beauty_types[2] += 0

    if scars == "true":
        beauty_types[2] += 0

    """BEE 3"""
    if skin_type and skin_condition == "Normal":
        beauty_types[3] += 50

    if acne == "true":
        beauty_types[3] += 0

    if aging == "true":
        beauty_types[3] += 0

    if clogged == "true":
        beauty_types[3] += 0

    if dryness == "true":
        beauty_types[3] += 0

    if dullness == "true":
        beauty_types[3] += 0

    if irritated == "true":
        beauty_types[3] += 0

    if oiliness == "true":
        beauty_types[3] += 0

    if scars == "true":
        beauty_types[3] += 0

    """BUTTERFLY 4"""
    if skin_type and skin_condition == "Dry":
        beauty_types[4] += 50

    if acne == "true":
        beauty_types[4] += 0

    if aging == "true":
        beauty_types[4] += 0

    if clogged == "true":
        beauty_types[4] += 0

    if dryness == "true":
        beauty_types[4] += 0

    if dullness == "true":
        beauty_types[4] += 0

    if irritated == "true":
        beauty_types[4] += 0

    if oiliness == "true":
        beauty_types[4] += 0

    if scars == "true":
        beauty_types[4] += 0

    """DRAGONFLY 5"""
    if skin_type and skin_condition == "Dehydrated":
        beauty_types[5] += 50

    if acne == "true":
        beauty_types[5] += 0

    if aging == "true":
        beauty_types[5] += 0

    if clogged == "true":
        beauty_types[5] += 0

    if dryness == "true":
        beauty_types[5] += 0

    if dullness == "true":
        beauty_types[5] += 0

    if irritated == "true":
        beauty_types[5] += 0

    if oiliness == "true":
        beauty_types[5] += 0

    if scars == "true":
        beauty_types[5] += 0

    print beauty_types

    sorted_beauty_types = sorted(beauty_types.items(), key=operator.itemgetter(1))
    print sorted_beauty_types

    user.skin_type = skin_type
    user.skin_condition = skin_condition

    # deletes any row in user_concern table mapping this user to that concern, clears out info from uc table
    User_Concern.query.filter_by(user_id=user_id).delete()
    db.session.commit()
    # create user concern w/concern id of 1 and user_id of user_id
    if acne:
        acne = User_Concern(user_id=user_id, concern_id=1)
        db.session.add(acne)
    if aging:
        aging = User_Concern(user_id=user_id, concern_id=2)
        db.session.add(aging)
    if clogged:
        clogged = User_Concern(user_id=user_id, concern_id=3)
        db.session.add(clogged)
    if dryness:
        dryness = User_Concern(user_id=user_id, concern_id=4)
        db.session.add(dryness)
    if dullness:
        dullness = User_Concern(user_id=user_id, concern_id=5)
        db.session.add(dullness)
    if irritated:
        irritated = User_Concern(user_id=user_id, concern_id=6)
        db.session.add(irritated)
    if oiliness:
        oiliness = User_Concern(user_id=user_id, concern_id=7)
        db.session.add(oiliness)
    if scars:
        scars = User_Concern(user_id=user_id, concern_id=8)
        db.session.add(scars)

    print "assigning beauty type", sorted_beauty_types[-1][0]
    user.beauty_type_id = sorted_beauty_types[-1][0]
    db.session.add(user)
    db.session.commit()

    flash("Profile submitted.")
    return redirect("/users/%s" % user.user_id)


@app.route("/users/<int:user_id>", methods=['GET'])
def user_detail(user_id):
    """Show user profile - linked from profile and login submission."""
    """Includes info from profile form & Beauty Type if user has taken profile form."""
    """Show list of any Products the User has Rated, sorted by the User & Product passed."""

    user = User.query.get(user_id)
    if session.get("user_id") != user.user_id:
        flash("User does not exist. Please try again")
        return redirect("/login")

    return render_template("user.html", user=user)


@app.route("/beauty_type/<int:beauty_type_id>")
def beauty_type_results(beauty_type_id):
    """Shows results of profile form, the Beauty Type assigned to the user. Linked from user.html (after they fill out profile form)"""
    """Includes a list of Product Categories filtered by the Beauty Type passed."""

    user_id = session.get("user_id")
    user = User.query.get(user_id)
    beauty_type = Beauty_Type.query.get(beauty_type_id)
    product_categories = Product_Category.query.order_by(Product_Category.product_category_id).all()

    return render_template("beauty_type.html", product_categories=product_categories, beauty_type=beauty_type, user=user)


@app.route("/product_categories/<int:beauty_type_id>/<int:product_category_id>")
def product_categories(beauty_type_id, product_category_id):
    """Show list of real life Products, filtered by the Beauty Type & Product Category passed. Linked from beauty_type.html."""

    beauty_type = Beauty_Type.query.get(beauty_type_id)
    print beauty_type.products
    product_category = Product_Category.query.get(product_category_id)
    products = Product.query.filter_by(beauty_type_id=beauty_type_id, product_category_id=product_category_id).all()
    return render_template("product_categories.html", beauty_type=beauty_type, product_category=product_category, products=products)


@app.route("/product/<int:product_id>", methods=['GET'])
def product_detail(product_id):
    """Show individual Product details. Allow user to rate & comment. Display ratings & comments from other users."""

    user_id = session.get("user_id")
    product = Product.query.get(product_id)
    # today = datetime.date.today()

    #Get the user's product rating & comment if they have already rated it.
    #Else, don't show a rating & comment.

    if user_id:
        user_rating = Rating.query.filter_by(
            product_id=product_id, user_id=user_id).first()

    else:
        user_rating = None

    # Get average rating of product

    rating_scores = [r.score for r in product.ratings]

    if len(rating_scores) > 0:
        avg_rating = float(sum(rating_scores)) / len(rating_scores)
    else:
        avg_rating = 0

    return render_template("product_detail.html", product=product, user_rating=user_rating, average=avg_rating)


@app.route("/product/<int:product_id>", methods=['POST'])
def rate_product(product_id):

    score = int(request.form["score"])
    comment = request.form["comment"]

    user_id = session.get("user_id")
    if not user_id:
        raise Exception("You are not logged in.")

    rating = Rating.query.filter_by(user_id=user_id, product_id=product_id).first()
    # comment = Rating.query.filter_by(user_id=user_id, product_id=product_id).first()

    if rating:
        rating.score = score
        flash("Your rating has been updated!")

    else:
        rating = Rating(user_id=user_id, product_id=product_id, score=score)
        flash("Your rating has been added!")
        db.session.add(rating)

    if comment:
        rating.comment = comment
        flash("Your comment has been updated!")

    else:
        comment = Rating(user_id=user_id, product_id=product_id, comment=comment)
        flash("Your commment has been added!")
        db.session.add(comment)

    db.session.commit()

    return redirect("/product/%s" % product_id)


@app.route("/all_products")
def all_products(product_id):
    """Show list of all products in the DB sorted by Product Category"""

    # beauty_type = Beauty_Type.query.get(beauty_type_id)
    # product = Product.query.get(product_id)
    products = Product.query.filter_by(product_id).all()
    return render_template("all_products.html", products=products, product_id=product_id)


# @app.route("/reddit", methods=['GET'])
# def get_top_reddit():
#     """Search asian beauty subreddit for products"""

#     connect to reddit api
#     user_agent = "glowbb"
#     r = praw.Reddit(user_agent=user_agent)
#     submissions = r.get_subreddit('asianbeauty').get_hot(limit=10)
#     get top 10 submissions in asianbeauty subreddit
#     for result in submissions:
#     for submissions in r.get_subreddit('asianbeauty').get_hot(limit=10):

    # get_content('http://www.reddit.com/r/AsianBeauty/', params=keyword, limit=25, place_holder=None, root_field='data', thing_field='children', after_field='after', _use_oauth=False, object_filter=None)
    # query = 'url:title'
    # search(query, subreddit='asianbeauty', sort=None, syntax=None, period=year, *args, **kwargs)

    # user_agent = "glowbb"
    # r = praw.Reddit(user_agent=user_agent)
    # query = 'url:title'
    # submissions = r.search(query=query, subreddit='asianbeauty', sort='hot', period='month', limit=100)
    # posts = []
    # for submission in submissions:
    #     post_obj = {
    #         'title': submissions.title,
    #         'url': submissions.url
    #     }
    #     posts.append(post_obj)
    # return jsonify({'posts': posts})

#     return render_template('reddit.html', r=r, submissions=submissions, posts=posts, query=query)

# CLIENT_ID = 'YOUR_CLIENT_ID'
# CLIENT_SECRET = 'YOUR CLIENT SECRET'
# REDIRECT_URI = 'http://127.0.0.1:65010/authorize_callback'

# print "\n\n\n%s\n\n\n" % r
# print "\n\n\n%s\n\n\n" % submissions

# @app.route('/')
# def homepage():
#     link_no_refresh = r.get_authorize_url('UniqueKey')
#     link_refresh = r.get_authorize_url('DifferentUniqueKey',
#                                        refreshable=True)
#     link_no_refresh = "<a href=%s>link</a>" % link_no_refresh
#     link_refresh = "<a href=%s>link</a>" % link_refresh
#     text = "First link. Not refreshable %s</br></br>" % link_no_refresh
#     text += "Second link. Refreshable %s</br></br>" % link_refresh
#     return text

# @app.route('/authorize_callback')
# def authorized():
#     state = request.args.get('state', '')
#     code = request.args.get('code', '')
#     info = r.get_access_information(code)
#     user = r.get_me()
#     variables_text = "State=%s, code=%s, info=%s." % (state, code,
#                                                       str(info))
#     text = 'You are %s and have %u link karma.' % (user.name,
#                                                    user.link_karma)
#     back_link = "<a href='/'>Try again</a>"
#     return variables_text + '</br></br>' + text + '</br></br>' + back_link


    # if submissions:
    #     results = Product.query.filter(or_(Product.description.ilike('%{}%'.format(submissions)), Product.product_name.ilike('%{}%'.format(submissions)), Product.product_brand.ilike('%{}%'.format(submissions)))).all()

    # else:
    #     results = None


# class praw.__init__.Reddit(*args, **kwargs)
#     get_content(url, params=None, limit=10, place_holder=None, root_field='data', thing_field='children', after_field='after', _use_oauth=False, object_filter=None)


@app.route('/add_product', methods=['GET'])
def add_product_form():
    """Show form for adding products to DB."""

    user_id = session.get("user_id")

    if not user_id:
        flash("User must be logged in.")
        return redirect("/login")

    return render_template("add_product.html")


@app.route('/add_product', methods=['POST'])
def add_product_process():
    """Process form for adding products to the DB."""

    # Get add_product form variables
    product_brand = request.form.get("product_brand")
    product_name = request.form.get("product_name")
    price = int(request.form.get("price"))
    description = request.form.get("description")
    product_category = request.form.get("product_category")
    beauty_type = request.form.get("beauty_type")

    concern_id = request.form.get("concern")
    print '\n\n\n%s\n\n\n\n' % concern_id

    new_product = Product(
        product_brand=product_brand,
        product_name=product_name,
        price=price,
        description=description,
        product_category_id=product_category,
        beauty_type_id=beauty_type,
        concern_id=concern_id
        )

    # Adds the new product to the database. Session of connection to DB.
    db.session.add(new_product)
    db.session.commit()

    # Browser/cookie storing session
    session["product_id"] = new_product.product_id

    flash("Your product submission has been received. Thank you!")
    return redirect("/product_categories/%s/%s" % (beauty_type, product_category))


@app.route('/search', methods=['GET'])
def search_form():
    """Show search form & results (if any). Searches Product brand, name & description."""

    q = request.args.get('q', '')
    if q:
        results = Product.query.filter(or_(Product.description.ilike('%{}%'.format(q)), Product.product_name.ilike('%{}%'.format(q)), Product.product_brand.ilike('%{}%'.format(q)))).all()

    else:
        results = None

    return render_template("search.html", results=results, q=q)


@app.route('/routine')
def plan_routine():
    """Plan Your Routine"""

    return render_template('routine.html')


if __name__ == "__main__":
    # We have to set debug=True here, since it has to be True at the point
    # that we invoke the DebugToolbarExtension
    # app.debug = True

    connect_to_db(app)

    # Use the DebugToolbar
    # DebugToolbarExtension(app)

    app.run()