# scripts/test_db.py
import sys
import os
sys.path.append(os.path.dirname(__file__))

from db import init_db, save_repos, cleanup_old

if __name__ == "__main__":
    print("Инициализация БД...")
    init_db()
    
    print("Очистка старых записей...")
    cleanup_old()
    
    print("Сохранение тестового репозитория...")
    test_repo = [{
        "name": "test/repo",
        "description": "Тестовый репозиторий",
        "url": "https://github.com/test/repo",
        "stars": 0,
        "created_at": "2025-12-26T00:00:00Z"
    }]
    save_repos(test_repo)
    
    print("Тест завершён.")