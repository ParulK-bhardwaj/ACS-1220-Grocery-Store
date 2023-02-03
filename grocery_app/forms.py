from flask_wtf import FlaskForm
from wtforms import StringField, FloatField, SelectField, SubmitField
from wtforms.ext.sqlalchemy.fields import QuerySelectField
from wtforms.validators import DataRequired, Length, URL
from wtforms.fields.html5  import DateField
from grocery_app.models import ItemCategory, GroceryItem, GroceryStore

class GroceryStoreForm(FlaskForm):
    """Form for adding/updating a GroceryStore."""
    title = StringField("Store Name",
        validators=[
            DataRequired(),
            Length(min=3, max=80, message="The store name needs to be between 3 and 80 chars")
        ])
    address = StringField("Address",
            validators=[
            Length(min=0, max=200, message="The address needs to be between 3 and 200 chars")
        ])
    submit = SubmitField("Submit")

class GroceryItemForm(FlaskForm):
    """Form for adding/updating a GroceryItem."""
    name = StringField("Prodcut Name",
        validators=[
            DataRequired(),
            Length(min=3, max=80, message= "The product name needs to be between 3 to 80 charcaters")
        ])
    price = FloatField("Price")
    category = SelectField("Category", choices=ItemCategory.choices())
    photo_url = StringField("Photo URL")
    store = QuerySelectField("Store",
        query_factory=lambda: GroceryStore.query, allow_blank=False)
    submit = SubmitField("Submit")

