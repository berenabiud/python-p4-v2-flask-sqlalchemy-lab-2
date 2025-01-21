from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import MetaData
from sqlalchemy.ext.associationproxy import association_proxy
from sqlalchemy_serializer import SerializerMixin


metadata = MetaData(naming_convention={
    "fk": "fk_%(table_name)s_%(column_0_name)s_%(referred_table_name)s",
})

db = SQLAlchemy(metadata=metadata)

from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.ext.associationproxy import association_proxy

db = SQLAlchemy()

class Customer(db.Model):
    __tablename__ = 'customers'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String)
    reviews = db.relationship('Review', back_populates='customer')
    items = association_proxy('reviews', 'item')  # Proxy to access items via reviews

    def __repr__(self):
        return f'<Customer {self.id}, {self.name}>'

    def to_dict(self):
        # First, ensure that reviews are populated before attempting to access items
        if self.reviews:
            items = [item for review in self.reviews for item in [review.item] if item]
        else:
            items = []

        return {
            'id': self.id,
            'name': self.name,
            'reviews': [{'id': review.id, 'comment': review.comment} for review in self.reviews],  # Serialize only necessary fields
            'items': [{'id': item.id, 'name': item.name} for item in items] if items else []  # Safely handle items
        }


class Item(db.Model):
    __tablename__ = 'items'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String)
    price = db.Column(db.Float)
    reviews = db.relationship('Review', back_populates='item')

    def __repr__(self):
        return f'<Item {self.id}, {self.name}, {self.price}>'

    def to_dict(self):
        return {
            'id': self.id,
            'name': self.name,
            'price': self.price,
            'reviews': [{'id': review.id, 'comment': review.comment} for review in self.reviews]  # Serialize only the necessary fields
        }


class Review(db.Model):
    __tablename__ = 'reviews'

    id = db.Column(db.Integer, primary_key=True)
    comment = db.Column(db.String)
    customer_id = db.Column(db.Integer, db.ForeignKey('customers.id'))
    item_id = db.Column(db.Integer, db.ForeignKey('items.id'))

    customer = db.relationship('Customer', back_populates='reviews')
    item = db.relationship('Item', back_populates='reviews')

    def __repr__(self):
        return f'<Review {self.id}, Customer {self.customer_id}, Item {self.item_id}, Comment {self.comment}>'

    def to_dict(self):
        return {
            'id': self.id,
            'comment': self.comment,
            'customer': {'id': self.customer.id, 'name': self.customer.name} if self.customer else {},  # Serialize only necessary fields
            'item': {'id': self.item.id, 'name': self.item.name} if self.item else {}  # Serialize only necessary fields
        }
