"""Glow Petite"""

from jinja2 import StrictUndefined

from flask import Flask, render_template, redirect, request, flash, session
from flask_debugtoolbar import DebugToolbarExtension

from model import connect_to_db, db


app = Flask(__name__)

# Required to use Flask sessions and the debug toolbar
app.secret_key = "ABC"

# Normally, if you use an undefined variable in Jinja2, it fails silently.
# This is horrible. Fix this so that, instead, it raises an error.
app.jinja_env.undefined = StrictUndefined


@app.route('/')
def index():
    """Homepage."""

    return render_template("homepage.html")


@app.route('/registration', methods=['GET'])
def register_form():

    return render_template("registration.html")


@app.route('/registration', methods=['POST'])
def register_process():

    email = request.form["email"]
    password = request.form["password"]
    zipcode = request.form["zipcode"]

    new_user = User(email=email, password=password, age=age, zipcode=zipcode)

    db.session.add(new_user)
    db.session.commit()

    flash("User %s added." % email)
    return redirect("/")


@app.route('/profile', methods=['GET'])
def profile_form():

        return render_template("profile_form.html")


@app.route('/profile', methods=['POST'])
def profile_process():

    skin_type = request.form["skin_type"]
    skin_concern = request.form["skin_concern"]
    age = int(request.form["age"])
    environment = request.form["environment"]

    new_profile = User(skin_type=skin_type, skin_concern=skin_concern, age=age, zipcode=zipcode)

    db.session.add(new_profile)
    db.session.commit()

    flash("Profile submitted.")
    return redirect("/")


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
    return redirect ("/")

"""Route below is to page that shows list of users."""
# @app.route("/users")
# def user_list():
#     """Show list of users."""

#     users = User.query.all()
#     return render_template("user_list.html", users=users)


@app.route("/users/<int:user_id>")
def user_detail(user_id):
    """Show user profile."""

    user = User.query.get(user_id)
    return render_template("user.html", user=user)


@app.route("/movies")
def movie_list():
    """Show list of movies."""

    movies = Movie.query.order_by(Movie.title).all()


    return render_template("movie_list.html", movies=movies)


@app.route("/movies/<int:movie_id>", methods=['GET'])
def movie_detail(movie_id):
    

    movie = Movie.query.get(movie_id)

    user_id = session.get("user_id")

    if user_id:
        user_rating = Rating.query.filter_by(
            movie_id=movie_id, user_id=user_id).first()

    else:
        user_rating = None

    # Get average rating of movie

    rating_scores = [r.score for r in movie.ratings]
    avg_rating = float(sum(rating_scores)) / len(rating_scores)

    prediction = None

    # Prediction code: only predict if the user hasn't rated it.

    # if (not user_rating) and user_id:
    #     user = User.query.get(user_id)
    #     if user:
    #         prediction = user.predict_rating(movie)

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

    # # Get the eye's rating, either by predicting or using real rating

    # the_eye = User.query.filter_by(email="the-eye@of-judgment.com").one()
    # eye_rating = Rating.query.filter_by(
    #     user_id=the_eye.user_id, movie_id=movie.movie_id).first()

    # if eye_rating is None:
    #     eye_rating = the_eye.predict_rating(movie)

    # else:
    #     eye_rating = eye_rating.score

    # if eye_rating and effective_rating:
    #     difference = abs(eye_rating - effective_rating)

    # else:
    #     # We couldn't get an eye rating, so we'll skip difference
    #     difference = None

    # # Depending on how different we are from the Eye, choose a message

    # BERATEMENT_MESSAGES = [
    #     "I suppose you don't have such bad taste after all.",
    #     "I regret every decision that I've ever made that has brought me" +
    #         " to listen to your opinion.",
    #     "Words fail me, as your taste in movies has clearly failed you.",
    #     "That movie is great. For a clown to watch. Idiot.",
    #     "Words cannot express the awfulness of your taste."
    # ]

    # if difference is not None:
    #     beratement = BERATEMENT_MESSAGES[int(difference)]

    # else:
    #     beratement = None

    # return render_template(
    #     "movie.html",
    #     movie=movie,
    #     user_rating=user_rating,
    #     average=avg_rating,
    #     prediction=prediction,
    #     eye_rating=eye_rating,
    #     difference=difference,
    #     beratement=beratement
    #     )


@app.route("/movies/<int:movie_id>", methods=['POST'])
def rate_movie(movie_id):

    score = int(request.form["score"])

    user_id = session.get("user_id")
    if not user_id:
        raise Exception("You are not logged in.")

    rating = Rating.query.filter_by(user_id=user_id, movie_id=movie_id).first()

    if rating:
        rating.score = score
        flash ("Your rating has been updated!")

    else:
        rating = Rating(user_id=user_id, movie_id=movie_id, score=score)
        flash("Your rating has been added!")
        db.session.add(rating)

    db.session.commit()

    return redirect("/movies/%s" % movie_id)

if __name__ == "__main__":
    # We have to set debug=True here, since it has to be True at the point
    # that we invoke the DebugToolbarExtension
    app.debug = True

    connect_to_db(app)

    # Use the DebugToolbar
    DebugToolbarExtension(app)

    app.run()