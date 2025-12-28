# scripts/fetch_github_repos.py
"""
Скрипт для получения новых публичных репозиториев на GitHub,
созданных за последние 3 дня, с упоминанием DevOps-ключевых слов.
"""

import requests
from datetime import datetime, timedelta
import os
import json


def get_devops_repos():
    """
    Запрашивает GitHub Search API и возвращает список репозиториев,
    созданных за последние 3 дня, содержащих 'devops', 'automation' или 'ci/cd'
    в названии или описании.
    """
    # Используем 3 дня вместо 1 — больше шансов найти что-то
    three_days_ago = (datetime.utcnow() - timedelta(days=3)).strftime('%Y-%m-%d')

    # Простой и рабочий запрос: ищем ключевые слова в названии/описании
    query = f"created:>={three_days_ago} " \
            "(devops OR automation OR 'ci/cd' OR kubernetes OR terraform) " \
            "in:name,description " \
            "language:yaml,language:python"

    print(f"🔍 Используемый запрос: {query}")

    url = "https://api.github.com/search/repositories"
    params = {
        "q": query,
        "sort": "stars",
        "order": "desc",
        "per_page": 30
    }

    # Заголовки с токеном (если есть)
    headers = {}
    github_token = os.getenv("GH_PAT")
    print(f"🔧 Токен: {'[УСТАНОВЛЕН]' if github_token else '[ОТСУТСТВУЕТ]'}")
    if github_token:
        headers["Authorization"] = f"token {github_token}"

    # Делаем запрос
    response = requests.get(url, params=params, headers=headers)
    print(f"📡 Статус: {response.status_code}")

    if response.status_code != 200:
        print(f"❌ Ошибка: {response.text}")
        return []

    data = response.json()
    total = data.get("total_count", 0)
    print(f"📦 Найдено: {total} репозиториев")

    repos = []
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
    repos = get_devops_repos()
    print(f"\n✅ Найдено: {len(repos)} репозиториев для сохранения")
    if repos:
        print(json.dumps(repos[:2], indent=2, ensure_ascii=False))