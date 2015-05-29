"""Glow Petite"""

from jinja2 import StrictUndefined
from flask import Flask, render_template, redirect, request, flash, session
from flask_debugtoolbar import DebugToolbarExtension
from model import connect_to_db, db, User, User_Concern, Concern, Specialty, Spec_PC, Product_Category, Product, Rating
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

    # Adds the new user to the database.
    db.session.add(new_user)
    db.session.commit()

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

    # user = User.query.get(user_id)

    return render_template("profile_form.html")


@app.route('/profile', methods=['POST'])
def profile_process():

    # Gets profile form variables and adds them to user_id.
    #Q1: Gets user's skin type (dropdown)
    skin_type = request.form.get("skin_type")
    #Q2: Allows user to select up to 3 skin "concerns" from list (checkbox)
    acne = request.form.get("acne")
    aging = request.form.get("aging")
    blackheads = request.form.get("blackheads")
    dryness = request.form.get("dryness")
    oiliness = request.form.get("oiliness")
    redness = request.form.get("redness")
    scars = request.form.get("scars")
    sensitivity = request.form.get("sensitivity")
    sun = request.form.get("sun")
    #Q3: Gets the user's age range (i.e. 19-29) (radio)
    age = request.form.get("age")
    #Q4: Gets the user's location type (radio)
    location = request.form.get("location")
    #Q5: Gets the user's weather type (radio)
    weather = request.form.get("weather")

    user_id = session.get("user_id")

    #This says that the profile is only added if the user is logged in.
    #If they have submitted profile in past, it overwrites those results with new results.
    #If not, it directs them to login.

    #Fine as long as this is an existing user submitting profile form (not for their 1st time)
    #But if this user is registering and then submitting profile for 1st time ever,
    #it will direct them to login after hitting submit on profile (instead of taking them to user page/results)
    #and it will NOT add the profile form data to the DB.

    if not user_id:
        flash("User does not exist. Please try again")
        return redirect("/login")
    print '\n\n\nhi  3\n\n\n'
    user = User.query.get(user_id)

    #weight types to see which is scored higher?


    # scores_for_user_answers = [skin_type, age, location, weather, acne, aging, blackheads, dryness, oiliness, redness, scars, sensitivity, sun]
    # user_score = 0
    # for i in scores_for_user_answers:
    #     user_score += i

        # create age, location & weather answer key
        # age_answer_key = {'under_18': 1} key = string related to form, value = value for that answer twd the score

    # user_answers = {'skin_type': skin_type, 'age': age, 'location': location, 'weather': weather}
    # #calculate here

#dictionary with all 9 specialties/types as the keys and the values as 0 for each (for now)
    specialties = {
        1: 0,  # "the happy person/kathy"
        2: 0,
        3: 0,
        4: 0,
        5: 0,
        6: 0,
        7: 0,
        8: 0,
        9: 0, }

    if oiliness:
        specialties[3] += 1

    if oiliness and age == '19-29':
        specialties[2] += 3

    print specialties

    sorted_specialties = sorted(specialties.items(), key=operator.itemgetter(1))
    print sorted_specialties

#go through all the info in the profile form and increment all 9 types based upon info
#when I'm done, the values will be an integer. then sort the "specialties" dict above
#to get the highest value for each. that highest value for each will be my "specialty/type",
#I can then direct the user twd their specialty/type

#weight every answer and set it to specialty
    # if oily:
    #     specialties[1] += 1

    # if combination:
    #     specialties[2] += 1

    # if normal:
    #     specialties[3] += 1

    # if dry:
    #     specialties[4] += 1

    # if dehydrated:
    #     specialties[5] += 1

    # if sensitive:
    #     specialties[6] += 1


            #at the very end go through dict and find value that is highest, that will be end user's specialty
            #sort dictionary at the end -- gives me specialyt # at the very end, assign it to the user, then save

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
    # db.session.add(user)
    print '\n\n\nhi  4\n\n\n'
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


    #dict w/all types as keys, values as 0 to start, go thru info in form, and 
    #based on info increment all 9 types, once i'm done values will be some 
    #integer and I'll sort to get highest value, highest value will be my 
    #specialty type, I can direct user to specialty type

    print "assigning user specialty", sorted_specialties[0][1]
    user.specialty_id = sorted_specialties[0][1]
    db.session.add(user)
    db.session.commit()

    flash("Profile submitted.")
    return redirect("/users/<int:user_id>")


"""Route to page that shows user profile with profile results (specialty). 
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