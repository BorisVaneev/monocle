from flask import Flask, render_template, request, redirect, url_for, session
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import check_password_hash
from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user, current_user

app = Flask(__name__)
app.config['SECRET_KEY'] = 'your_secret_key'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'
db = SQLAlchemy(app)
login_manager = LoginManager(app)
login_manager.login_view = 'login'


class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(150), unique=True, nullable=False)
    password = db.Column(db.String(150), nullable=False)


class MenuItem(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    store_id = db.Column(db.String(100), nullable=False)
    name = db.Column(db.String(100), nullable=False)
    description = db.Column(db.String(300))
    price = db.Column(db.Float, nullable=False)
    category = db.Column(db.String(100), nullable=False)
    photo_url = db.Column(db.String(300))
    menu_id = db.Column(db.String(100))


class Order(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    store_id = db.Column(db.String(100), nullable=False)
    table_number = db.Column(db.Integer, nullable=False)
    items = db.Column(db.String(500), nullable=False)  # Just a simple text of ordered items


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


@app.route('/admin', methods=['GET', 'POST'])
def admin_login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        user = User.query.filter_by(username=username).first()
        if user and check_password_hash(user.password, password):
            login_user(user)
            return redirect(url_for('admin_dashboard'))
    return render_template('admin_login.html')


@app.route('/admin/dashboard')
@login_required
def admin_dashboard():
    return render_template('dashboard.html')


@app.route('/store/<store_id>/menuconstructor', methods=['GET', 'POST'])
@login_required
def menuconstructor(store_id):
    if request.method == 'POST':
        name = request.form['name']
        description = request.form['description']
        price = request.form['price']
        category = request.form['category']
        photo_url = request.form['photo_url']
        menu_id = request.form['menu_id']
        menu_item = MenuItem(store_id=store_id, name=name, description=description, price=price, category=category,
                             photo_url=photo_url, menu_id=menu_id)
        db.session.add(menu_item)
        db.session.commit()
        return redirect(url_for('menuconstructor', store_id=store_id))
    menu_items = MenuItem.query.filter_by(store_id=store_id).all()
    return render_template('menuconstructor.html', store_id=store_id, menu_items=menu_items)


@app.route('/store/<store_id>/menu<menu_id>/<table_id>')
def menu(store_id, menu_id, table_id):
    menu_items = MenuItem.query.filter_by(store_id=store_id, menu_id=menu_id).all()
    return render_template('menu.html', store_id=store_id, menu_id=menu_id, table_id=table_id, menu_items=menu_items)


@app.route('/store/<store_id>/dashboard')
@login_required
def store_dashboard(store_id):
    orders = Order.query.filter_by(store_id=store_id).all()
    return render_template('dashboard.html', orders=orders)


if __name__ == '__main__':
    db.create_all()
    app.run(debug=True)
