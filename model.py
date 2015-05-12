"""Models and database functions for Skincare Profiler & Product Finder."""

from flask_sqlalchemy import SQLAlchemy

import correlation

# This is the connection to the SQLite database; we're getting this through
# the Flask-SQLAlchemy helper library. On this, we can find the `session`
# object, where we do most of our interactions (like committing, etc.)

db = SQLAlchemy()


##############################################################################
# Model definitions

class User(db.Model):
    """User of application."""

    __tablename__ = "users"

    user_id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    email = db.Column(db.String(64), nullable=True)
    password = db.Column(db.String(64), nullable=True)
    age = db.Column(db.Integer, nullable=True)
    zipcode = db.Column(db.String(15), nullable=True)
    user_type = db.Column(db.Integer, db.ForeignKey('types.type_id'))

    def __repr__(self):
        """provide helpful representation when printed"""
        return "<User user_id=%s email=%s user_type=%s>" %
        (self.user_id, self.email, self.user_type)


class Type(db.Model):
    """User type - code received upon filling out profile."""

    __tablename__ = "types"

    user_type = db.Column(db.Integer, autoincrement=True, primary_key=True)
    type_name = db.Column(db.String(64), nullable=True)


    """Use Pearson rating to find something? How other users in their area,
    age group, etc. scored?"""

    # def similarity(self, other):
    # # """Return Pearson rating for user compared to other user."""

    #     u_ratings = {}
    #     paired_ratings = []

    #     for r in self.ratings:
    #         u_ratings[r.movie_id] = r

    #     for r in other.ratings:
    #         u_r = u_ratings.get(r.movie_id)
    #         if u_r:
    #             paired_ratings.append( (u_r.score, r.score) )

    #     if paired_ratings:
    #         return correlation.pearson(paired_ratings)

    #     else:
    #         return 0.0

    # def predict_rating(self, movie):
    #     # """Predict user's rating of a movie."""

    #     other_ratings = movie.ratings

    #     similarities = [
    #         (self.similarity(r.user), r)
    #         for r in other_ratings
    #     ]

    #     similarities.sort(reverse=True)

    #     similarities = [(sim, r) for sim, r in similarities if sim > 0]

    #     if not similarities:
    #         return None

    #     numerator = sum([r.score * sim for sim, r in similarities])
    #     denominator = sum([sim for sim, r in similarities])

    #     return numerator/denominator


class Product_Category(db.Model):
    __tablename__ = "product_categories"

    """General categories of various products."""

    product_category_id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    product_category_name = db.Column(db.String(64), nullable=True)
    user_type = db.Column(db.Integer, db.ForeignKey('types.type_id'))


class Product(db.Model):
    __tablename__ = "products"

    product_id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    sku = db.Column(db.String(64), nullable=True)
    product_category_name = db.Column(db.String(64), nullable=True)
    price = db.Column(db.Integer)
    description = db.Column(db.String(1000), nullable=True)
    image = db.Column(db.Blob, nullable=True)
    product_category_id = db.Column(db.Integer, db.ForeignKey('product_categories.product_category_id'))
    user_id = db.Column(db.Integer, db.ForeignKey('users.user_id'))

     # Define relationship to user
    user = db.relationship('User', backref=db.backref('types', order_by=user_type)

    # Define relationship to product category
    product_category = db.relationship('Product_Category', backref=db.backref('types', order_by=user_type))

    # Define relationship to product
    product = db.relationship('Product', backref=db.backref('product_categories', order_by=product_categories_id))


def __repr__(self):
        """Provide helpful representation when printed."""

        return "<Type user_type=%s user_id=%s product_category_id=%s type_name=%s>" % (
            self.user_type, self.user_id, self.product_category_id, self.type_name)



##############################################################################
# Helper functions

def connect_to_db(app):
    """Connect the database to our Flask app."""

    # Configure to use our SQLite database
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///ratings.db'
    db.app = app
    db.init_app(app)


if __name__ == "__main__":
    # As a convenience, if we run this module interactively, it will leave
    # you in a state of being able to work with the database directly.

    from server import app
    connect_to_db(app)
    print "Connected to DB."