from flask import Blueprint, request, render_template, redirect, url_for, flash
from flask_login import login_user, logout_user, login_required, current_user
from grocery_app.models import GroceryStore, GroceryItem, User
from grocery_app.forms import GroceryStoreForm, GroceryItemForm, LoginForm, SignUpForm
# Import app and db from events_app package so that we can run app
from grocery_app.extensions import app, db, bcrypt

# Blueprints
main = Blueprint("main", __name__)
# We'll use this blueprint to define the routes for login & signup.
auth = Blueprint("auth", __name__)

##########################################
#           Routes                       #
##########################################

@main.route('/')
def homepage():
    all_stores = GroceryStore.query.all()
    print(all_stores)
    return render_template('home.html', all_stores=all_stores)

@main.route('/new_store', methods=['GET', 'POST'])
@login_required
def new_store():
    # Created a GroceryStoreForm
    form = GroceryStoreForm()

    if form.validate_on_submit():
        new_store = GroceryStore(
            title=form.title.data,
            address=form.address.data,
            created_by=current_user
        )
        db.session.add(new_store)
        db.session.commit()

        flash("New store was created successfully.")
        return redirect(url_for("main.store_detail", store_id=new_store.id))

    return render_template('new_store.html', form=form)

@main.route('/new_item', methods=['GET', 'POST'])
@login_required
def new_item():
    # Created a GroceryItemForm
    form = GroceryItemForm()

    if form.validate_on_submit():
        new_item = GroceryItem(
            name=form.name.data,
            price=form.price.data,
            category=form.category.data,
            photo_url=form.photo_url.data,
            store=form.store.data,
            created_by=current_user
        )
        
        db.session.add(new_item)
        db.session.commit()

        flash("New item was created successfully.")
        return redirect(url_for("main.item_detail", item_id=new_item.id))

    return render_template('new_item.html', form=form)

@main.route('/store/<store_id>', methods=['GET', 'POST'])
@login_required
def store_detail(store_id):
    store = GroceryStore.query.get(store_id)

    # Created a GroceryStoreForm and pass in `obj=store`
    form = GroceryStoreForm(obj=store)

    if form.validate_on_submit():
        form.populate_obj(store)

        db.session.add(store)
        db.session.commit()
        flash("Store was updated successfully")
        return redirect(url_for("main.store_detail", store_id=store.id))
        
    store = GroceryStore.query.get(store_id)
    return render_template('store_detail.html',store=store, form=form)

@main.route('/item/<item_id>', methods=['GET', 'POST'])
@login_required
def item_detail(item_id):
    item = GroceryItem.query.get(item_id)
    # Created a GroceryItemForm and pass in `obj=item`
    form = GroceryItemForm(obj=item)
    if form.validate_on_submit():
        form.populate_obj(item)

        db.session.add(item)
        db.session.commit()
        flash("Item was updated successfully")
        return redirect(url_for("main.item_detail",item_id=item.id))

    item = GroceryItem.query.get(item_id)
    return render_template('item_detail.html', item=item, form=form)

# ... adds item to current_user's shopping list
@main.route('/add_to_shopping_list/<item_id>', methods=['POST'])
def add_to_shopping_list(item_id):
    item = GroceryItem.query.get(item_id)
    current_user.shopping_list_user.append(item)
    db.session.add(current_user)
    db.session.commit()
    flash("Item has been successfully added to the shopping list.")
    return redirect(url_for("main.shopping_list"))

# Stretch Challenge: removes item from current_user's shopping list
@main.route('/remove_from_shopping_list/<item_id>', methods=['POST'])
def remove_from_shopping_list(item_id):
    item = GroceryItem.query.get(item_id)
    current_user.shopping_list_user.remove(item)
    db.session.add(current_user)
    db.session.commit()
    flash("Item has been successfully removed from the shopping list.")
    return redirect(url_for("main.shopping_list"))

# ... get logged in user's shopping list items ...
# ... display shopping list items in a template ...
@main.route('/shopping_list')
@login_required
def shopping_list():
    shopping_list = current_user.shopping_list_user
    return render_template('shopping_list.html', shopping_list=shopping_list)


# AUTH ROUTES
@auth.route('/signup', methods=['GET', 'POST'])
def signup():
    print('in signup')
    form = SignUpForm()
    if form.validate_on_submit():
        hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        user = User(
            username=form.username.data,
            password=hashed_password
        )
        db.session.add(user)
        db.session.commit()
        flash('Account Created.')
        print('created')
        return redirect(url_for('auth.login'))
    print(form.errors)
    return render_template('signup.html', form=form)


@auth.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        login_user(user, remember=True)
        next_page = request.args.get('next')
        return redirect(next_page if next_page else url_for('main.homepage'))
    return render_template('login.html', form=form)

@auth.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('main.homepage'))



