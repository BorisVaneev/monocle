from app import db
from flask_migrate import Migrate, upgrade

# Инициализация миграции
migrate = Migrate()

def run_migrations():
    try:
        upgrade()
        print("✅ Migration successful!")
    except Exception as e:
        print(f"❌ Migration failed: {e}")

if __name__ == '__main__':
    run_migrations()
