"""Models and database functions for Skincare Profiler & Product Finder."""

from flask_sqlalchemy import SQLAlchemy

# import correlation

# This is the connection to the SQLite database; we're getting this through
# the Flask-SQLAlchemy helper library. On this, we can find the `session`
# object, where we do most of our interactions (like committing, etc.)

db = SQLAlchemy()


##############################################################################
# Model definitions

class User(db.Model):
    """User of skincare website + Profile."""

    __tablename__ = "users"

    user_id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    email = db.Column(db.String(64), nullable=True)
    password = db.Column(db.String(64), nullable=True)
    firstname = db.Column(db.String(64), nullable=True)
    lastname = db.Column(db.String(64), nullable=True)
    zipcode = db.Column(db.String(15), nullable=True)
    specialty_id = db.Column(db.Integer, db.ForeignKey('specialties.specialty_id'))
    skin_type = db.Column(db.String(64), nullable=True)
    age = db.Column(db.Integer, nullable=True)
    location = db.Column(db.String(64), nullable=True)
    weather = db.Column(db.String(64), nullable=True)

    # Define relationship to specialty
    specialty = db.relationship("Specialty", backref=db.backref('users', order_by=user_id))

    def calculate_specialty_type(self):
        """In function have access to anything in User table"""

        # "if" statements for each profile-related thing in "User" table that tell me  the value for each answer "group".
        # if self.skin_type == "oily", self.skin_concern == "", self.age == "", self.location == "", self.weather == "":

        # Dictionary that assigns profile form scores to types:
        # specialties = {'0-10': 'Type 1', '11-20': 'Type 2', '21-30': 'Type 3', '31-40': 'Type 4',
        # '41-50': 'Type 5', '51-60': 'Type 6', '61-70': 'Type 7', '71-80': 'Type 8', '81-90': 'Type 9'}

        # #dictionary w/question to answer/value chunks, inner dict that says this answer is worth x points, & etc.

        # if self.skin_type == this and they have concerns x,y,z
        # run database query specialty = Specialty.query.filter_by
        # will need dict that says if have this # they will be type 1, etc.
        # if have this # their specialty_id is X (hardcode ids
        #     assign self.specialty_id
        #     once I've done calculation
        #     self.specialty_id = X)
        # big function with a ton of if statements for each thing in User table

        # Have to have user obj to run function
        # eg U = User.query.get(1)
        #     u.calculate_specialty_type() # to do all things, assign specialty, and then I can say
        #      "u.specialty" and it will give me the specialty from the table

    def __repr__(self):
        """Provide helpful representation when printed."""

        return "<User user_id=%s email=%s>" % (self.user_id, self.email)


class User_Concern(db.Model):
    """User/Concern Association Table."""

    __tablename__ = "user_concerns"

    uc_id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.user_id'))
    concern_id = db.Column(db.Integer, db.ForeignKey('concerns.concern_id'))
    # concern_name = db.Column(db.String(64), db.ForeignKey('concerns.concern_name'))

    # Define relationship to user
    user = db.relationship("User", backref=db.backref('user_concerns', order_by=uc_id))

    # Defines relationship to concern
    concern = db.relationship('Concern', backref=db.backref('user_concerns', order_by=uc_id))

    def __repr__(self):
        """Provide helpful representation when printed."""

        return "<User_Concern uc_id=%s user_id=%s concern_id=%s>" % (self.uc_id, self.user_id, self.concern_id)


class Concern(db.Model):
    """Concerns from profile form - user may select up to 3."""

    __tablename__ = "concerns"

    concern_id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    concern_name = db.Column(db.String(64), nullable=True)

    def __repr__(self):
        """Provide helpful representation when printed."""

        return "<Concern concern_id=%s concern_name=%s>" % (self.concern_id, self.concern_name)


class Specialty(db.Model):
    """User specialty/type - code received upon filling out profile."""

    __tablename__ = "specialties"

    specialty_id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    specialty_name = db.Column(db.String(64), nullable=True)

    def __repr__(self):
        """Provide helpful representation when printed."""

        return "<Specialty specialty_id=%s specialty_name=%s>" % (self.specialty_id, self.specialty_name)


class Spec_PC(db.Model):
    """Specialty/Product_Category Association Table."""

    __tablename__ = "specialty_pcs"

    spc_id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    specialty_id = db.Column(db.Integer, db.ForeignKey('specialties.specialty_id'))
    product_category_id = db.Column(db.Integer, db.ForeignKey('product_categories.product_category_id'))

    # Define relationship to specialty
    specialty = db.relationship("Specialty", backref=db.backref('specialties_pcs', order_by=spc_id))

    # Define relationship to product_category
    product_category = db.relationship('Product_Category', backref=db.backref('specialties_pcs', order_by=spc_id))

    def __repr__(self):
        """Provide helpful representation when printed."""

        return "<Specialty_PC spc_id=%s>" % (self.spc_id)


class Product_Category(db.Model):
    __tablename__ = "product_categories"

    """General categories of various products."""

    product_category_id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    product_category_name = db.Column(db.String(64), nullable=True)

    def __repr__(self):
        """Provide helpful representation when printed."""

        return "<Product_Category product_category_id=%s product_category_name=%s>" % (
            self.product_category_id, self.product_category_name)


class Product(db.Model):
    __tablename__ = "products"

    """Specific, real life products that fit in to each Product_Category"""

    product_id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    sku = db.Column(db.String(64), nullable=True)
    product_name = db.Column(db.String(64), nullable=True)
    price = db.Column(db.Integer)
    description = db.Column(db.String(1000), nullable=True)
    # image = db.Column(db.Blob, nullable=True)
    product_category_id = db.Column(db.Integer, db.ForeignKey('product_categories.product_category_id'))

    product_category = db.relationship('Product_Category', backref=db.backref('products', order_by=product_id))

    def __repr__(self):
        """Provide helpful representation when printed."""

        return "<Product product_id=%s sku=%s  product_name=%s price=%s description=%s product_category_id=%s>" % (
            self.product_id, self.sku, self.product_name, self.price, self.description, self.product_category_id)


class Rating(db.Model):
    __tablename__ = "ratings"

    """Users can rate many products. Products can be rated by many users (and have many ratings)."""

    rating_id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    product_id = db.Column(db.Integer, db.ForeignKey('products.product_id'))
    user_id = db.Column(db.Integer, db.ForeignKey('users.user_id'))
    score = db.Column(db.Integer)

     # Define relationship to user
    user = db.relationship('User', backref=db.backref('ratings', order_by=rating_id))

    # Define relationship to product
    product = db.relationship('Product', backref=db.backref('ratings', order_by=rating_id))

    def __repr__(self):
        """Provide helpful representation when printed."""

        return "<Rating rating_id=%s product_id=%s user_id=%s score=%s>" % (
            self.rating_id, self.product_id, self.user_id, self.score)


##############################################################################
# Helper functions
def connect_to_db(app):
    """Connect the database to our Flask app."""

    # Configure to use our SQLite database
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///glowpetite.db'
    db.app = app
    db.init_app(app)


if __name__ == "__main__":
    # As a convenience, if we run this module interactively, it will leave
    # you in a state of being able to work with the database directly.

    from server import app
    connect_to_db(app)
    print "Connected to DB."