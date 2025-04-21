from flask import Flask, render_template, request, redirect, url_for, session, flash
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate, upgrade, init
from flask_login import UserMixin, LoginManager, login_user, login_required, logout_user, current_user
import os

app = Flask(__name__)

# Настройка базы данных
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SECRET_KEY'] = 'your_secret_key'  # Для сессий и flash-сообщений

# Инициализация базы и миграций
db = SQLAlchemy(app)
migrate = Migrate(app, db)

# Инициализация Flask-Login
login_manager = LoginManager(app)
login_manager.login_view = "login"  # Переадресация на страницу логина, если пользователь не авторизован

# Модель пользователя
class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(100), unique=True, nullable=False)
    password = db.Column(db.String(100), nullable=False)
    is_admin = db.Column(db.Boolean, default=False)  # Флаг для суперпользователя

# Модель заказа
class Order(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    table_number = db.Column(db.Integer)
    menu_item = db.Column(db.String(255))

# Инициализация миграций
@app.before_first_request
def initialize_migrations():
    """This function will run migrations when the app starts."""
    if not os.path.exists('migrations'):
        init()  
    try:
        upgrade()  
        print("✅ Migrations applied successfully!")
    except Exception as e:
        print(f"❌ Migrations failed: {e}")

# Логика для загрузки пользователя
@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

# Страница логина для суперпользователя
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        user = User.query.filter_by(username=username).first()

        if user and user.password == password:  # Проверка пароля
            login_user(user)
            flash("Welcome, admin!", "success")
            return redirect(url_for('admin_dashboard'))
        else:
            flash("Invalid credentials. Please try again.", "danger")

    return render_template('admin_login.html')

# Панель администратора
@app.route('/admin', methods=['GET'])
@login_required
def admin_dashboard():
    if not current_user.is_admin:
        return redirect(url_for('index'))

    orders = Order.query.all()
    return render_template('dashboard.html', orders=orders)

# Выход из системы
@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('login'))

# Страница всех заказов
@app.route('/')
def index():
    orders = Order.query.all()
    return render_template('index.html', orders=orders)

# Страница меню для конкретного столика
@app.route('/store001/menu1/<int:table_number>', methods=['GET', 'POST'])
def menu(table_number):
    if request.method == 'POST':
        menu_item = request.form['menu_item']
        order = Order(table_number=table_number, menu_item=menu_item)
        db.session.add(order)
        db.session.commit()
        return redirect(url_for('index'))

    return render_template('menu.html', table_number=table_number)

if __name__ == '__main__':
    app.run(debug=True)
