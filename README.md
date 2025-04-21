# monocle
# Monocle Project

Monocle - это проект для создания и управления меню для ресторанов с возможностью оформления заказов через QR-коды.

## Как развернуть проект

1. Клонировать репозиторий:
   ```bash
   git clone https://github.com/BorisVaneev/monocle.git

Создать виртуальное окружение и активировать его:

bash
Копировать
Редактировать
python3 -m venv venv
source venv/bin/activate  # для Linux/macOS
venv\Scripts\activate   
Установить зависимости:

bash
Копировать
Редактировать
pip install -r requirements.txt

Создать файл .env и добавить туда настройки для базы данных и секретных ключей:

env
Копировать
Редактировать
FLASK_APP=app.py
FLASK_ENV=development
SECRET_KEY=your_secret_key
SQLALCHEMY_DATABASE_URI=sqlite:///database.db

Применить миграции:

bash
Копировать
Редактировать
flask db upgrade

Запустить приложение:

bash
Копировать
Редактировать
flask run

Примечания
Проект использует Flask и SQLAlchemy для работы с базой данных.

Для продакшн-сервера рекомендуется использовать более производительные базы данных, такие как PostgreSQL или MySQL.
