from sqlalchemy_utils import URLType

from grocery_app.extensions import db
from grocery_app.utils import FormEnum

class ItemCategory(FormEnum):
    """Categories of grocery items."""
    PRODUCE = 'Produce'
    DELI = 'Deli'
    BAKERY = 'Bakery'
    PANTRY = 'Pantry'
    FROZEN = 'Frozen'
    OTHER = 'Other'

class GroceryStore(db.Model):
    """Grocery Store model."""
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(80), nullable=False)
    address = db.Column(db.String(200), nullable=False)
    items = db.relationship('GroceryItem', back_populates='store')

    def __str__(self):
        return f"{self.title}"
    
    def __repr__(self):
        return f"<{self.id}:{self.title}>"

    # created_by_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    # created_by = db.relationship('User')

class GroceryItem(db.Model):
    """Grocery Item model."""
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), nullable=False)
    price = db.Column(db.Float(precision=2), nullable=False)

    # The category - What category the item relates to?
    category = db.Column(db.Enum(ItemCategory), default=ItemCategory.OTHER)
    photo_url = db.Column(URLType)
    store_id = db.Column(
        db.Integer, db.ForeignKey('grocery_store.id'), nullable=False)
    store = db.relationship('GroceryStore', back_populates='items')

    def __str__(self):
        return f"{self.name}"
    
    def __repr__(self):
        return f"<{self.id}:{self.name}>"


    # created_by_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    # created_by = db.relationship('User')

# class User(db.Model):
#     id = db.Column(db.Integer, primary_key=True)
#     username = db.Column(db.String(15), nullable=False)
#     password = db.Column(db.String(15), nullable=False)