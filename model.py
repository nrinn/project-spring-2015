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
    """User of skincare website."""

    __tablename__ = "users"

    user_id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    email = db.Column(db.String(64), nullable=True)
    password = db.Column(db.String(64), nullable=True)
    firstname = db.Column(db.String(64), nullable=True)
    lastname = db.Column(db.String(64), nullable=True)
    # age = db.Column(db.Integer, nullable=True)
    zipcode = db.Column(db.String(15), nullable=True)
    # specialty_id = db.Column(db.Integer, db.ForeignKey('specialties.specialty_id'))

    # # Defines relationship to Specialty (formerly "Type")
    # specialty = db.relationship("Specialty", backref=db.backref('users', order_by='user_id'))

    def __repr__(self):
        """Provide helpful representation when printed."""

        return "<User user_id=%s email=%s>" % (self.user_id, self.email)

    # class Profile(db.Model):
    #     """User profile."""

    # __tablename__ = "profiles"

    # profile_id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    # email = db.Column(db.String(64), nullable=True)
    # password = db.Column(db.String(64), nullable=True)
    # firstname = db.Column(db.String(64), nullable=True)
    # lastname = db.Column(db.String(64), nullable=True)
    # # age = db.Column(db.Integer, nullable=True)
    # zipcode = db.Column(db.String(15), nullable=True)
    # # specialty_id = db.Column(db.Integer, db.ForeignKey('specialties.specialty_id'))

    # # # Defines relationship to Specialty (formerly "Type")
    # # specialty = db.relationship("Specialty", backref=db.backref('users', order_by='user_id'))

    # def __repr__(self):
    #     """Provide helpful representation when printed."""

    #     return "<User user_id=%s email=%s>" % (self.user_id, self.email)


class Specialty(db.Model):
    """User specialty/type - code received upon filling out profile."""

    __tablename__ = "specialties"

    specialty_id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    specialty_name = db.Column(db.String(64), nullable=True)

    def __repr__(self):
        """Provide helpful representation when printed."""

        return "<Specialty specialty_id=%s specialty_name=%s>" % (self.specialty_id, self.specialty_name)


class Product_Category(db.Model):
    __tablename__ = "product_categories"

    """General categories of various products."""

    product_category_id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    product_category_name = db.Column(db.String(64), nullable=True)
    # specialty_id = db.Column(db.Integer, db.ForeignKey('specialties.specialty_id'))

    # specialty = db.relationship('Specialty', backref=db.backref('product_categories', order_by='product_category_id'))

    def __repr__(self):
        """Provide helpful representation when printed."""

        return "<Product_Category product_category_id=%s product_category_name=%s specialty_id=%s>" % (
            self.product_category_id, self.product_category_name, self.specialty_id)


class Product(db.Model):
    __tablename__ = "products"

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

    rating_id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    product_id = db.Column(db.Integer, db.ForeignKey('products.product_id'))
    user_id = db.Column(db.Integer, db.ForeignKey('users.user_id'))
    score = db.Column(db.Integer)

     # Define relationship to user
    user = db.relationship('User', backref=db.backref('ratings', order_by=rating_id))

    # Define relationship to movie
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