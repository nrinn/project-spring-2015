"""Glow Petite"""

from jinja2 import StrictUndefined

from flask import Flask, render_template, redirect, request, flash, session
from flask_debugtoolbar import DebugToolbarExtension

from model import connect_to_db, db, User, Specialty, Product_Category, Product


app = Flask(__name__)

# Required to use Flask sessions and the debug toolbar
app.secret_key = "ABC"

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

        return render_template("profile_form.html")


@app.route('/profile', methods=['POST'])
def profile_process():

    skin_type = request.form["skin_type"]
    skin_concern = request.form["skin_concern"]
    age = int(request.form["age"])
    location = request.form["location"]
    weather = request.form["weather"]

    new_profile = User(skin_type=skin_type, skin_concern=skin_concern, age=age, location=location, weather=weather)

    db.session.add(new_profile)
    db.session.commit()

    flash("Profile submitted.")
    return redirect("/users/<int:user_id>")


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