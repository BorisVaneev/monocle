from flask import Flask, render_template, request, redirect
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)

# Настройка SQLite базы данных
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

# Главная страница
@app.route('/')
def index():
    orders = db.session.execute('SELECT * FROM order').fetchall()  # Получаем все заказы
    return render_template('index.html', orders=orders)

# Страница меню
@app.route('/store001/menu1/<int:table_number>', methods=['GET', 'POST'])
def menu(table_number):
    if request.method == 'POST':
        menu_item = request.form['menu_item']
        db.session.execute('INSERT INTO order (table_number, menu_item) VALUES (?, ?)', 
                           (table_number, menu_item))
        db.session.commit()  # Сохраняем в базе данных
        return redirect('/')  # Перенаправляем на главную страницу

    return render_template('menu.html', table_number=table_number)

# Создание таблиц при запуске приложения
@app.before_first_request
def create_tables():
    db.session.execute('''
        CREATE TABLE IF NOT EXISTS order (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            table_number INTEGER,
            menu_item TEXT
        )
    ''')
    db.session.commit()

if __name__ == "__main__":
    app.run(debug=True)
