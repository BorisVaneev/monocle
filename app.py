from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate, upgrade, init
import os

app = Flask(__name__)

# Настройки для продакшн-сервера и базы данных
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('SQLALCHEMY_DATABASE_URI', 'sqlite:///database.db')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY', 'your_default_secret_key')

# Инициализация базы и миграций
db = SQLAlchemy(app)
migrate = Migrate(app, db)

# Модель базы данных
class Order(db.Model):
    id = db.Column(db.Integer, primary_key=True)  # Идентификатор заказа
    table_number = db.Column(db.Integer)          # Номер столика
    menu_item = db.Column(db.String(255))         # Позиция меню

# Главная страница
@app.route('/')
def index():
    try:
        orders = Order.query.all()  # Получаем все заказы
        return render_template('index.html', orders=orders)
    except Exception as e:
        return f"Ошибка при получении заказов: {e}"

# Страница меню
@app.route('/store001/menu1/<int:table_number>', methods=['GET', 'POST'])
def menu(table_number):
    try:
        if request.method == 'POST':
            menu_item = request.form['menu_item']
            order = Order(table_number=table_number, menu_item=menu_item)
            db.session.add(order)
            db.session.commit()
            return redirect(url_for('index'))
        return render_template('menu.html', table_number=table_number)
    except Exception as e:
        return f"Ошибка при добавлении заказа: {e}"

# Панель администратора
@app.route('/admin', methods=['GET'])
def admin_dashboard():
    try:
        orders = Order.query.all()
        return render_template('admin.html', orders=orders)
    except Exception as e:
        return f"Ошибка при получении заказов для админа: {e}"

# Выполнение миграций
@app.before_first_request
def initialize_migrations():
    """This function will run migrations when the app starts."""
    if not os.path.exists('migrations'):
        init()  # Инициализация миграций, если их нет
    try:
        upgrade()  # Выполнение миграций
        print("✅ Migrations applied successfully!")
    except Exception as e:
        print(f"❌ Migrations failed: {e}")

if __name__ == '__main__':
    app.run(debug=False)  # Отключаем debug для продакшн
