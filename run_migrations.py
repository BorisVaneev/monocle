from app import db
from flask_migrate import Migrate, upgrade
from app import app  # Импортируем объект Flask-приложения

# Инициализация миграции
migrate = Migrate(app, db)  # Передаем app и db в Migrate

def run_migrations():
    try:
        upgrade()  # Запуск миграций
        print("✅ Migration successful!")
    except Exception as e:
        print(f"❌ Migration failed: {e}")

if __name__ == '__main__':
    run_migrations()
