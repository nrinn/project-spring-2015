"""Glow Petite"""

from jinja2 import StrictUndefined

from flask import Flask, render_template, redirect, request, flash, session
from flask_wtf import Form, validators
from wtforms import FloatField
from wtforms.validators import NumberRange
from flask_debugtoolbar import DebugToolbarExtension

from model import connect_to_db, db, User, User_Concern, Concern, Specialty, Spec_PC, Product_Category, Product, Rating


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

    # Get form variables
    email = request.form["email"]
    password = request.form["password"]
    firstname = request.form["firstname"]
    lastname = request.form["lastname"]
    # age = int(request.form["age"])
    zipcode = request.form["zipcode"]

    new_user = User(email=email, password=password, firstname=firstname, lastname=lastname, zipcode=zipcode)

    db.session.add(new_user)
    db.session.commit()

    flash("User %s added." % email)
    return redirect("/profile")


@app.route('/login', methods=['GET'])
def login_form():

    return render_template("login_form.html")


@app.route('/login', methods=['POST'])
def login_process():

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
    return redirect("/users/%s" % user.user_id)


@app.route('/logout')
def logout():

    del session["user_id"]
    flash("You have logged out.")
    return redirect("/")


@app.route('/profile', methods=['GET'])
def profile_form():

    # user = User.query.get(user_id)

    return render_template("profile_form.html")


@app.route('/profile', methods=['POST'])
def profile_process():
    # import pdb; pdb.set_trace()
    # print '\n\n\n%s\n\n\n' % request.form
    skin_type = request.form.get("skin_type")
    acne = request.form.get("acne")
    aging = request.form.get("aging")
    blackheads = request.form.get("blackheads")
    dryness = request.form.get("dryness")
    oiliness = request.form.get("oiliness")
    redness = request.form.get("redness")
    scars = request.form.get("scars")
    sensitivity = request.form.get("sensitivity")
    sun = request.form.get("sun")
    # age = int(request.form["age"])
    age = request.form.get("age")
    location = request.form.get("location")
    weather = request.form.get("weather")
    # print '\n\n\nhi  1\n\n\n'
    user_id = session.get("user_id")
    # print '\n\n\nhi  2\n\n\n'
    if not user_id:
        flash("User does not exist. Please try again")
        return redirect("/login")
    # print '\n\n\nhi  3\n\n\n'
    user = User.query.get(user_id)
    scores_for_user_answers = [skin_type, age, location, weather, acne, aging, blackheads, dryness, oiliness, redness, scars, sensitivity, sun]
    user_score = 0
    for i in scores_for_user_answers:
        user_score += i

        # create age, location & weather answer key
        # age_answer_key = {'under_18': 1} key = string related to form, value = value for that answer twd the score

    # user_answers = {'skin_type': skin_type, 'age': age, 'location': location, 'weather': weather}
    # #calculate here

    # skin_type_answers = {
    #     'oily': 1 # 1 is the value of that answer for that question. when all values are added it = specialty/type
    # }

    # age_answers = {
    #     'under_18': 1
    # }

    # location_answers = {
    #     'urban': 1
    # }

    # weather_answers = {
    #     'humid': 1
    # }

    # answer_key = {'skin_type': skin_type_answers, 'age': age_answers, 'location': location_answers, 'weather': weather_answers}
    # user_score = 0
    # for answer in user_answers.iteritems(): #iteritems = can do a for loop over a dict
    #     score_for_this_question = answer_key[answer[0]][answer[1]]
    #     user_score += score_for_this_question
    #     # goes through all answers and adds value for each answer to user_score

   # update, don't create, use . syntax:
   # user.skintype = thing from form, for stuff on user table it all gets added once b/c it is once per object
    user.skin_type = skin_type
    user.age = age
    user.location = location
    user.weather = weather
    db.session.add(user)
    # print '\n\n\nhi  4\n\n\n'
   # new_profile = User(skin_type=skin_type, age=age, location=location, weather=weather)

    # concern = Concern.query.filter_by(concern_name=concern_name.lower()).all()

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
    if blackheads:
        blackheads = User_Concern(user_id=user_id, concern_id=3)
        db.session.add(blackheads)
    if dryness:
        dryness = User_Concern(user_id=user_id, concern_id=4)
        db.session.add(dryness)
    if oiliness:
        oiliness = User_Concern(user_id=user_id, concern_id=5)
        db.session.add(oiliness)
    if redness:
        redness = User_Concern(user_id=user_id, concern_id=6)
        db.session.add(redness)
    if scars:
        scars = User_Concern(user_id=user_id, concern_id=7)
        db.session.add(scars)
    if sensitivity:
        sensitivity = User_Concern(user_id=user_id, concern_id=8)
        db.session.add(sensitivity)
    if sun:
        sun = User_Concern(user_id=user_id, concern_id=9)
        db.session.add(sun)

    db.session.commit()

    flash("Profile submitted.")
    return redirect("/specialties/<int:specialty_id>")

"""Route to page that shows single user's profile results."""


@app.route("/specialties/<int:specialty_id>", methods=['GET'])
def profile_results(specialty_id):
    """Show user's profile results (specialty)."""

    specialty = Specialty.query.get(specialty_id)
    return render_template("specialty.html", specialty=specialty)

#     user_id = session.get("user_id")
#     profile_score = session.get("profile_score")

    # Here is where I will define what profile scores = each type.
    # e.g. if profile_score < 50 and > 40:
    #           specialty_name = type 5

#     if profile_score


#     if user_id:
#         user_rating = Rating.query.filter_by(
#             movie_id=movie_id, user_id=user_id).first()

#     else:
#         user_rating = None

#     Get average rating of movie

#     rating_scores = [r.score for r in movie.ratings]
#     avg_rating = float(sum(rating_scores)) / len(rating_scores)

#     prediction = None


# @app.route("/movies/<int:movie_id>", methods=['POST'])
# def rate_movie(movie_id):

#     score = int(request.form["score"])

#     user_id = session.get("user_id")
#     if not user_id:
#         raise Exception("You are not logged in.")

#     rating = Rating.query.filter_by(user_id=user_id, movie_id=movie_id).first()

#     if rating:
#         rating.score = score
#         flash ("Your rating has been updated!")

#     else:
#         rating = Rating(user_id=user_id, movie_id=movie_id, score=score)
#         flash("Your rating has been added!")
#         db.session.add(rating)

#     db.session.commit()

#     return redirect("/movies/%s" % movie_id)

"""Route to page that shows single movie's profile. Also checks to see if
user is logged in, has reviewed movie yet, etc."""
# @app.route("/movies/<int:movie_id>", methods=['GET'])
# def movie_detail(movie_id):


#     movie = Movie.query.get(movie_id)

#     user_id = session.get("user_id")

#     if user_id:
#         user_rating = Rating.query.filter_by(
#             movie_id=movie_id, user_id=user_id).first()

#     else:
#         user_rating = None

    # Get average rating of movie

    # rating_scores = [r.score for r in movie.ratings]
    # avg_rating = float(sum(rating_scores)) / len(rating_scores)

    # prediction = None


# @app.route("/movies/<int:movie_id>", methods=['POST'])
# def rate_movie(movie_id):

#     score = int(request.form["score"])

#     user_id = session.get("user_id")
#     if not user_id:
#         raise Exception("You are not logged in.")

#     rating = Rating.query.filter_by(user_id=user_id, movie_id=movie_id).first()

#     if rating:
#         rating.score = score
#         flash ("Your rating has been updated!")

#     else:
#         rating = Rating(user_id=user_id, movie_id=movie_id, score=score)
#         flash("Your rating has been added!")
#         db.session.add(rating)

#     db.session.commit()

#     return redirect("/movies/%s" % movie_id)


"""Route to page that shows list of users."""
# @app.route("/users")
# def user_list():
#     """Show list of users."""

#     users = User.query.all()
#     return render_template("user_list.html", users=users)


"""Route to page that shows user profile."""


@app.route("/users/<int:user_id>")
def user_detail(user_id):
    """Show user profile."""

    user = User.query.get(user_id)
    return render_template("user.html", user=user)

    """Route to page that shows list of all specialties."""
# @app.route("/specialties")
# def specialty_list():
#     """Show list of all specialties."""

#     specialty = Specialty.query.order_by(Specialty.specialty_name).all()


#     return render_template("specialty_list.html", specialties=specialties)

"""Route to page that shows single specialty profile."""
# @app.route("/specialties/<int:specialty_id>")
# def specialty_detail(specialty_id):
#     """Show specialty profile."""

#     specialty = Specialty.query.get(specialty_id)
#     return render_template("specialty.html", specialty=specialty)


"""Route to page that shows list of product_categories."""
# @app.route("/product_categories")
# def product_category_list():
#     """Show list of product_categories."""

#     product_category = Product_Category.query.order_by(Product_Category.product_category_name).all()


#     return render_template("product_category_list.html", product_categories=product_categories)


"""Route to page that shows a product category's list of real products."""
# @app.route("/real_product_list")
# def real_product_list():
#     """Show list of real-life products that fit into that product category"""

#     product = Product.query.order_by(Product.product_name).all()


#     return render_template("real_product_list.html", products=products)


"""Route to page that shows single movie's profile. Also checks to see if
user is logged in, has reviewed movie yet, etc."""
# @app.route("/movies/<int:movie_id>", methods=['GET'])
# def movie_detail(movie_id):


#     movie = Movie.query.get(movie_id)

#     user_id = session.get("user_id")

#     if user_id:
#         user_rating = Rating.query.filter_by(
#             movie_id=movie_id, user_id=user_id).first()

#     else:
#         user_rating = None

    # Get average rating of movie

    # rating_scores = [r.score for r in movie.ratings]
    # avg_rating = float(sum(rating_scores)) / len(rating_scores)

    # prediction = None


# @app.route("/movies/<int:movie_id>", methods=['POST'])
# def rate_movie(movie_id):

#     score = int(request.form["score"])

#     user_id = session.get("user_id")
#     if not user_id:
#         raise Exception("You are not logged in.")

#     rating = Rating.query.filter_by(user_id=user_id, movie_id=movie_id).first()

#     if rating:
#         rating.score = score
#         flash ("Your rating has been updated!")

#     else:
#         rating = Rating(user_id=user_id, movie_id=movie_id, score=score)
#         flash("Your rating has been added!")
#         db.session.add(rating)

#     db.session.commit()

#     return redirect("/movies/%s" % movie_id)

if __name__ == "__main__":
    # We have to set debug=True here, since it has to be True at the point
    # that we invoke the DebugToolbarExtension
    app.debug = True

    connect_to_db(app)

    # Use the DebugToolbar
    DebugToolbarExtension(app)

    app.run()