"""Snail Love"""

from jinja2 import StrictUndefined
from flask import Flask, render_template, redirect, request, flash, session
from flask_debugtoolbar import DebugToolbarExtension
from model import connect_to_db, db, User, User_Concern, Concern, Beauty_Type, Beauty_Type_Category, Product_Category, Product, Rating
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

    # Takes the user to their user page when they login.
    return redirect("/users/%s" % user.user_id)


@app.route('/logout')
def logout():

    del session["user_id"]
    flash("You have logged out.")
    return redirect("/")


@app.route('/profile', methods=['GET'])
def profile_form():

    user_id = session.get("user_id")

    if not user_id:
        flash("User must be logged in.")
        return redirect("/login")

    user = User.query.get(user_id)

    return render_template("profile_form.html")


@app.route('/profile', methods=['POST'])
def profile_process():

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

#go through all the info in the profile form and increment all 9 types based upon info
#when I'm done, the values will be an integer. then sort the "beauty_types" dict above
#to get the highest value for each. that highest value for each will be my "beauty type",
#I can then direct the user twd their beauty type.

#weight every answer and set it to beauty type.


#at the very end go through dict and find value that is highest, that will be end user's beauty type
#sort dictionary at the end -- gives me beauty type # at the very end, assign it to the user, then save

    # skin_type_answers = {
    #     'oily': 1 # 1 is the value of that answer for that question. when all values are added it = beauty type
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


"""Route to page that shows user profile with profile results (beauty type). 
Profile submit button always brings you here, whether it is your 1st time 
filling out the form or your 10th. """


@app.route("/users/<int:user_id>")
def user_detail(user_id):
    """Show user profile."""

    user = User.query.get(user_id)
    return render_template("user.html", user=user)


if __name__ == "__main__":
    # We have to set debug=True here, since it has to be True at the point
    # that we invoke the DebugToolbarExtension
    app.debug = True

    connect_to_db(app)

    # Use the DebugToolbar
    DebugToolbarExtension(app)

    app.run()