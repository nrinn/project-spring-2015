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
    """User of skin care product finder website."""

    __tablename__ = "users"

    user_id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    email = db.Column(db.String(64), nullable=True)
    password = db.Column(db.String(64), nullable=True)
    age = db.Column(db.Integer, nullable=True)
    zipcode = db.Column(db.String(15), nullable=True)
    user_type_id = db.Column(db.Integer, db.ForeignKey('types.user_type_id'))

    user_type_id = db.relationship('Type', backref=db.backref('users', order_by='user_id'))

    def __repr__(self):
        """provide helpful representation when printed"""
        return "<User user_id=%s email=%s user_type_id=%s>" % (self.user_id, self.email, self.user_type_id)


class Type(db.Model):
    """User type - code received upon filling out profile."""

    __tablename__ = "types"

    user_type_id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    type_name = db.Column(db.String(64), nullable=True)


class Product_Category(db.Model):
    __tablename__ = "product_categories"

    """General categories of various products."""

    product_category_id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    product_category_name = db.Column(db.String(64), nullable=True)
    user_type_id = db.Column(db.Integer, db.ForeignKey('types.user_type_id'))

    types = db.relationship('Type', backref=db.backref('product_categories', order_by='product_category_id'))


class Product(db.Model):
    __tablename__ = "products"

    product_id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    sku = db.Column(db.String(64), nullable=True)
    product_category_name = db.Column(db.String(64), nullable=True)
    price = db.Column(db.Integer)
    description = db.Column(db.String(1000), nullable=True)
    # image = db.Column(db.Blob, nullable=True)
    product_category_id = db.Column(db.Integer, db.ForeignKey('product_categories.product_category_id'))
    product_category = db.relationship('Product_Category', backref=db.backref('products', order_by=product_id))


def __repr__(self):
        """Provide helpful representation when printed."""

        return "<Type user_type_id=%s user_id=%s product_category_id=%s type_name=%s>" % (
            self.user_type_id, self.user_id, self.product_category_id, self.type_name)


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