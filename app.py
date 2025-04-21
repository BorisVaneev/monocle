from flask import Flask, render_template, request, redirect, url_for, flash, session
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from werkzeug.security import generate_password_hash, check_password_hash
import os

app = Flask(__name__)

# Настройка SQLite базы данных
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SECRET_KEY'] = 'your_secret_key'

# Инициализация базы и миграций
db = SQLAlchemy(app)
migrate = Migrate(app, db)

# Суперпользователь (пароль и логин известны только вам)
SUPERUSER_USERNAME = 'admin'
SUPERUSER_PASSWORD_HASH = generate_password_hash('superpassword', method='sha256')  # Пароль для суперпользователя

# Модель базы данных
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(100), unique=True, nullable=False)
    password = db.Column(db.String(100), nullable=False)

# Модель для заказов
class Order(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    table_number = db.Column(db.Integer)
    menu_item = db.Column(db.String(255))

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        # Проверяем, является ли это суперпользователем
        if username == SUPERUSER_USERNAME and check_password_hash(SUPERUSER_PASSWORD_HASH, password):
            session['logged_in'] = True
            return redirect(url_for('admin_dashboard'))
        
        # Если не суперпользователь, проверяем, есть ли такой пользователь в базе данных
        user = User.query.filter_by(username=username).first()
        if user and check_password_hash(user.password, password):
            session['logged_in'] = True
            return redirect(url_for('user_dashboard'))

        flash('Invalid credentials', 'danger')

    return render_template('admin_login.html')

@app.route('/admin', methods=['GET'])
def admin_dashboard():
    # Проверяем, что это суперпользователь
    if 'logged_in' not in session:
        return redirect(url_for('login'))

    users = User.query.all()
    return render_template('admin_dashboard.html', users=users)

@app.route('/add_user', methods=['GET', 'POST'])
def add_user():
    if 'logged_in' not in session:
        return redirect(url_for('login'))

    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        hashed_password = generate_password_hash(password, method='sha256')
        new_user = User(username=username, password=hashed_password)
        db.session.add(new_user)
        db.session.commit()
        flash('User added successfully!', 'success')
        return redirect(url_for('admin_dashboard'))

    return render_template('add_user.html')

@app.route('/logout')
def logout():
    session.pop('logged_in', None)
    return redirect(url_for('login'))

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8000)
