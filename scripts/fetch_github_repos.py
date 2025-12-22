# scripts/fetch_github_repos.py
"""
Скрипт для получения новых публичных репозиториев на GitHub,
созданных за последние 24 часа, по ключевым словам, связанным с DevOps.
Результат: список словарей с данными репозиториев.
"""

import requests
from datetime import datetime, timedelta
import json


def get_devops_repos():
    """
    Запрашивает GitHub Search API и возвращает список репозиториев,
    созданных за последние 24 часа, содержащих DevOps-ключи в описании или названии.
    """
    # 1. Вычисляем дату 24 часа назад в формате YYYY-MM-DD
    yesterday = (datetime.utcnow() - timedelta(days=1)).strftime('%Y-%m-%d')

    # 2. Формируем запрос: ищем репозитории, созданные после вчерашней даты
    #    и содержащие хотя бы одно из ключевых слов
    query = (
        f"created:>{yesterday} "
        "language:yaml,language:json,language:shell,language:python "
        "topic:devops topic:automation topic:ci topic:cd topic:kubernetes topic:terraform"
    )

    # 3. URL GitHub Search API
    url = "https://api.github.com/search/repositories"
    params = {
        "q": query,
        "sort": "stars",
        "order": "desc",
        "per_page": 30  # Получаем максимум 30 репозиториев (лимит API)
    }

    # 4. Делаем запрос
    response = requests.get(url, params=params)

    if response.status_code != 200:
        print(f"Ошибка GitHub API: {response.status_code} - {response.text}")
        return []

    data = response.json()
    repos = []

    # 5. Извлекаем только нужные поля
    for item in data.get("items", []):
        repos.append({
            "name": item["full_name"],
            "description": item["description"] or "",
            "url": item["html_url"],
            "stars": item["stargazers_count"],
            "created_at": item["created_at"]
        })

    return repos


if __name__ == "__main__":
    # Запуск скрипта напрямую — для теста
    repos = get_devops_repos()
    print(f"Найдено {len(repos)} репозиториев:")
    print(json.dumps(repos[:3], indent=2, ensure_ascii=False))  # Показываем первые 3
