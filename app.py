from flask import Flask, render_template, redirect, url_for, request, flash
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user, current_user

app = Flask(__name__)

# Настройки базы данных
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///users.db'  # SQLite база данных
app.config['SECRET_KEY'] = 'supersecretkey'  # Секретный ключ для сессий
db = SQLAlchemy(app)

# Инициализация Flask-Login
login_manager = LoginManager()
login_manager.init_app(app)

# Модели
class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(150), unique=True, nullable=False)
    password = db.Column(db.String(150), nullable=False)

class Store(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(150), nullable=False)
    owner_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    owner = db.relationship('User', backref=db.backref('stores', lazy=True))

# Загрузка пользователя
@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

# Страница логина
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        user = User.query.filter_by(username=username).first()

        if user and user.password == password:  # Проверка пароля
            login_user(user)
            return redirect(url_for('admin_dashboard'))
        else:
            flash('Неверный логин или пароль')
    return render_template('admin_login.html')

# Страница логина администратора
@app.route('/admin_dashboard')
@login_required
def admin_dashboard():
    if current_user.username != 'admin':  # Только для суперюзера
        return redirect(url_for('login'))
    stores = Store.query.all()
    return render_template('admin_dashboard.html', stores=stores)

# Страница добавления пользователя (заведения)
@app.route('/add_user', methods=['GET', 'POST'])
@login_required
def add_user():
    if current_user.username != 'admin':  # Только для суперюзера
        return redirect(url_for('login'))
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        new_user = User(username=username, password=password)
        db.session.add(new_user)
        db.session.commit()
        flash('Новый пользователь добавлен')
        return redirect(url_for('admin_dashboard'))
    return render_template('add_user.html')

# Страница выхода
@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('login'))

if __name__ == '__main__':
    app.run(debug=True)
