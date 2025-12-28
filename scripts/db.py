# scripts/db.py
"""
Модуль для работы с PostgreSQL.
Поддерживает: инициализацию БД, сохранение репозиториев, очистку старых записей.
"""

import os
import psycopg2
from psycopg2.extras import RealDictCursor
from dotenv import load_dotenv

# Загружаем переменные из .env (локально)
load_dotenv()

def get_db_connection():
    """Создаёт подключение к PostgreSQL."""
    return psycopg2.connect(
        host=os.getenv("DB_HOST", "localhost"),
        port=os.getenv("DB_PORT", "5432"),
        database=os.getenv("DB_NAME", "trends"),
        user=os.getenv("DB_USER", "devops_analyzer"),
        password=os.getenv("DB_PASSWORD", ""),
    )

def init_db():
    """Создаёт таблицу repos, если её нет."""
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute("""
        CREATE TABLE IF NOT EXISTS repos (
            id SERIAL PRIMARY KEY,
            name TEXT UNIQUE NOT NULL,
            description TEXT,
            url TEXT,
            stars INTEGER,
            created_at TIMESTAMP,
            fetched_at TIMESTAMP DEFAULT NOW()
        );
    """)
    conn.commit()
    cur.close()
    conn.close()
    print("Таблица 'repos' готова.")

def save_repos(repos):
    """Сохраняет список репозиториев в БД. Игнорирует дубликаты (по name)."""
    if not repos:
        return

    conn = get_db_connection()
    cur = conn.cursor()
    for repo in repos:
        try:
            cur.execute("""
                INSERT INTO repos (name, description, url, stars, created_at)
                VALUES (%s, %s, %s, %s, %s)
                ON CONFLICT (name) DO NOTHING;
            """, (
                repo["name"],
                repo["description"],
                repo["url"],
                repo["stars"],
                repo["created_at"]
            ))
        except Exception as e:
            print(f"Ошибка при сохранении {repo['name']}: {e}")
    conn.commit()
    cur.close()
    conn.close()
    print(f"Сохранено {len(repos)} репозиториев.")

def cleanup_old():
    """Удаляет записи старше 30 дней."""
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute("DELETE FROM repos WHERE fetched_at < NOW() - INTERVAL '30 days';")
    deleted = cur.rowcount
    conn.commit()
    cur.close()
    conn.close()
    print(f"Удалено {deleted} устаревших записей.")