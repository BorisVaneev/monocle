from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
import os

app = Flask(__name__)

# Настройка SQLite базы данных
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

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
    orders = Order.query.all()  # Получаем все заказы
    return render_template('index.html', orders=orders)

# Страница меню
@app.route('/store001/menu1/<int:table_number>', methods=['GET', 'POST'])
def menu(table_number):
    if request.method == 'POST':
        menu_item = request.form['menu_item']
        order = Order(table_number=table_number, menu_item=menu_item)
        db.session.add(order)
        db.session.commit()
        return redirect(url_for('index'))

    return render_template('menu.html', table_number=table_number)

# Панель администратора
@app.route('/admin', methods=['GET'])
def admin_dashboard():
    orders = Order.query.all()
    return render_template('admin.html', orders=orders)

if __name__ == '__main__':
    app.run(debug=True)
