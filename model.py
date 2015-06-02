"""Models and database functions for Skin Care Profiler & Product Finder."""

from flask_sqlalchemy import SQLAlchemy

# import correlation

# This is the connection to the SQLite database; we're getting this through
# the Flask-SQLAlchemy helper library. On this, we can find the `session`
# object, where we do most of our interactions (like committing, etc.)

db = SQLAlchemy()


##############################################################################
# Model definitions

class User(db.Model):
    """User of skin care website + Profile."""

    __tablename__ = "users"

    user_id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    email = db.Column(db.String(64), nullable=True)
    password = db.Column(db.String(64), nullable=True)
    firstname = db.Column(db.String(64), nullable=True)
    lastname = db.Column(db.String(64), nullable=True)
    zipcode = db.Column(db.String(15), nullable=True)
    beauty_type_id = db.Column(db.Integer, db.ForeignKey('beauty_types.beauty_type_id'))
    skin_type = db.Column(db.String(64), nullable=True)

    # Define relationship to beauty_type
    beauty_type = db.relationship("Beauty_Type", backref=db.backref('users', order_by=user_id))

    def __repr__(self):
        """Provide helpful representation when printed."""

        return "<User user_id=%s email=%s>" % (self.user_id, self.email)


class User_Concern(db.Model):
    """User/Concern Association Table."""

    __tablename__ = "user_concerns"

    user_concern_id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.user_id'))
    concern_id = db.Column(db.Integer, db.ForeignKey('concerns.concern_id'))

    # Define relationship to user
    user = db.relationship("User", backref=db.backref('user_concerns', order_by=user_concern_id))

    # Defines relationship to concern
    concern = db.relationship('Concern', backref=db.backref('user_concerns', order_by=user_concern_id))

    def __repr__(self):
        """Provide helpful representation when printed."""

        return "<User_Concern user_concern_id=%s user_id=%s concern_id=%s>" % (self.user_concern_id, self.user_id, self.concern_id)

    # def similarity(self, other):
    # # """Return Pearson rating for user compared to other user."""

    #     u_ratings = {}
    #     paired_ratings = []

    #     for r in self.ratings:
    #         u_ratings[r.product_id] = r

    #     for r in other.ratings:
    #         u_r = u_ratings.get(r.product_id)
    #         if u_r:
    #             paired_ratings.append( (u_r.score, r.score) )

    #     if paired_ratings:
    #         return correlation.pearson(paired_ratings)

    #     else:
    #         return 0.0

    # def predict_rating(self, product):
    #     # """Predict user's rating of a product."""

    #     other_ratings = product.ratings

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


class Concern(db.Model):
    """Concerns from profile form - user may select up to 3."""

    __tablename__ = "concerns"

    concern_id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    concern_name = db.Column(db.String(64), nullable=True)

    def __repr__(self):
        """Provide helpful representation when printed."""

        return "<Concern concern_id=%s concern_name=%s>" % (self.concern_id, self.concern_name)


class Beauty_Type(db.Model):
    """Result user receives from profile."""

    __tablename__ = "beauty_types"

    beauty_type_id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    beauty_type_name = db.Column(db.String(64), nullable=True)

    def __repr__(self):
        """Provide helpful representation when printed."""

        return "<Beauty_Type beauty_type_id=%s beauty_type_name=%s>" % (self.beauty_type_id, self.beauty_type_name)


class Product_Category(db.Model):
    __tablename__ = "product_categories"

    """General categories of products as passed by assigned beauty type."""

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
    product_brand = db.Column(db.String(64), nullable=True)
    product_name = db.Column(db.String(64), nullable=True)
    price = db.Column(db.Integer)
    description = db.Column(db.String(1000), nullable=True)
    beauty_type_id = db.Column(db.Integer, db.ForeignKey('beauty_types.beauty_type_id'))
    product_category_id = db.Column(db.Integer, db.ForeignKey('product_categories.product_category_id'))

    beauty_type = db.relationship('Beauty_Type', backref=db.backref('products', order_by=product_id))
    product_category = db.relationship('Product_Category', backref=db.backref('products', order_by=product_id))

    def __repr__(self):
        """Provide helpful representation when printed."""

        return "<Product product_id=%s sku=%s product_brand=%s product_name=%s price=%s description=%s beauty_type_id=%s product_category_id=%s>" % (
            self.product_id, self.sku, self.product_brand, self.product_name, self.price, self.description, self.beauty_type_id, self.product_category_id)


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
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///snaillove.db'
    db.app = app
    db.init_app(app)


if __name__ == "__main__":
    # As a convenience, if we run this module interactively, it will leave
    # you in a state of being able to work with the database directly.

    from server import app
    connect_to_db(app)
    print "Connected to DB."