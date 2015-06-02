"""Snail Love"""

from jinja2 import StrictUndefined
from flask import Flask, render_template, redirect, request, flash, session
from flask_debugtoolbar import DebugToolbarExtension
from model import connect_to_db, db, User, User_Concern, Concern, Beauty_Type, Product_Category, Product, Rating
import operator

app = Flask(__name__)

# Required to use Flask sessions and the debug toolbar
app.secret_key = "ABC"
app.debug = True

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

    user = User.query.get(user_id)

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
    #Q1: Gets user's skin type (dropdown)
    skin_type = request.form.get("skin_type")

    #Q2: Allows user to select up to 3 skin "concerns" from list (checkbox)
    acne = request.form.get("acne")
    aging = request.form.get("aging")
    dryness = request.form.get("dryness")
    dullness = request.form.get("dullness")
    oiliness = request.form.get("oiliness")
    scars = request.form.get("scars")

#dictionary with all 4 beauty types as the keys and the values as 0 for each (for now)
    beauty_types = {
        1: 0,  # oily (dewdrop)
        2: 0,  # combination
        3: 0,  # normal
        4: 0, }  # dry

    if skin_type == "oily":
        beauty_types[1] += 10

    if acne == "true":
        beauty_types[1] += 5

    if aging == "true":
        beauty_types[1] += 5

    if oiliness == "true":
        beauty_types[1] += 5

    if dullness == "true":
        beauty_types[4] += 100

    if skin_type == "dry":
        beauty_types[2] += 10

    print beauty_types

    sorted_beauty_types = sorted(beauty_types.items(), key=operator.itemgetter(1))
    print sorted_beauty_types

    user.skin_type = skin_type

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
    if dryness:
        dryness = User_Concern(user_id=user_id, concern_id=3)
        db.session.add(dryness)
    if dullness:
        dullness = User_Concern(user_id=user_id, concern_id=4)
        db.session.add(dullness)
    if oiliness:
        oiliness = User_Concern(user_id=user_id, concern_id=5)
        db.session.add(oiliness)
    if scars:
        scars = User_Concern(user_id=user_id, concern_id=6)
        db.session.add(scars)


    #dict w/all types as keys, values as 0 to start, go thru info in form, and 
    #based on info increment all 9 types, once i'm done values will be some 
    #integer and I'll sort to get highest value, highest value will be my 
    #beauty type, I can direct user to beauty type

    print "assigning beauty type", sorted_beauty_types[-1][0]
    user.beauty_type_id = sorted_beauty_types[-1][0]
    db.session.add(user)
    db.session.commit()

    flash("Profile submitted.")
    return redirect("/users/%s" % user.user_id)


@app.route("/users/<int:user_id>")
def user_detail(user_id):
    """Show user profile - linked from profile sumbission, and login submission."""

    user = User.query.get(user_id)

    return render_template("user.html", user=user)


@app.route("/beauty_type/<int:beauty_type_id>")
def beauty_type_results(beauty_type_id):
    """Shows results of profile form, the Beauty Type assigned to the user. Linked from user.html (after they fill out profile form)"""
    """Includes a list of Product Categories sorted by the Beauty Type passed."""
    # finds all product categories related to beauty_type_id (which is all of them)

    beauty_type = Beauty_Type.query.get(beauty_type_id)
    product_categories = Product_Category.query.order_by(Product_Category.product_category_id).all()

    return render_template("beauty_type.html", product_categories=product_categories, beauty_type=beauty_type)


@app.route("/product_list/<int:beauty_type_id>/<int:product_category_id>")
def product_list(product_category_id, beauty_type_id):
    """Show list of real life Products, sorted by the Product Category & Beauty Type passed. Linked from beauty_type.html."""

    beauty_type = Beauty_Type.query.get(beauty_type_id)
    product_category = Product_Category.query.get(product_category_id)
    products = Product.query.order_by(Product.product_name).all()
    return render_template("product_categories.html", beauty_type=beauty_type, product_category=product_category, products=products)


@app.route("/product/<int:product_id>", methods=['GET'])
def product_detail(product_id):
    """Show individual Product details. Linked from product_categories.html."""

    product = Product.query.get(product_id)
    user_id = session.get("user_id")

    if user_id:
        user_rating = Rating.query.filter_by(
            product_id=product_id, user_id=user_id).first()

    else:
        user_rating = None

    # Get average rating of product

    rating_scores = [r.score for r in product.ratings]
    avg_rating = float(sum(rating_scores)) / len(rating_scores)

    prediction = None

    # Prediction code: only predict if the user hasn't rated it yet.

    # if (not user_rating) and user_id:
    #     user = User.query.get(user_id)
    #     if user:
    #         prediction = user.predict_rating(product)

    # # Either use the prediction or their real rating

    # if prediction:
    #     # User hasn't scored; use our prediction if we made one
    #     effective_rating = prediction

    # elif user_rating:
    #     # User has already scored for real; use that
    #     effective_rating = user_rating.score

    # else:
    #     # User hasn't scored, and we couldn't get a prediction
    #     effective_rating = None

    return render_template("product_detail.html", product=product, user_rating=user_rating, average=avg_rating, prediction=prediction)


@app.route("/product/<int:product_id>", methods=['POST'])
def rate_product(product_id):

    score = int(request.form["score"])

    user_id = session.get("user_id")
    if not user_id:
        raise Exception("You are not logged in.")

    rating = Rating.query.filter_by(user_id=user_id, product_id=product_id).first()

    if rating:
        rating.score = score
        flash("Your rating has been updated!")

    else:
        rating = Rating(user_id=user_id, product_id=product_id, score=score)
        flash("Your rating has been added!")
        db.session.add(rating)

    db.session.commit()

    return redirect("/product/%s" % product_id)


if __name__ == "__main__":
    # We have to set debug=True here, since it has to be True at the point
    # that we invoke the DebugToolbarExtension
    app.debug = True

    connect_to_db(app)

    # Use the DebugToolbar
    DebugToolbarExtension(app)

    app.run()