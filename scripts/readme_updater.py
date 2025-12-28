# scripts/readme_updater.py
"""
Модуль для обновления секции с трендами в README.md
"""

import os

def generate_markdown_table(repos):
    """Генерирует Markdown-таблицу из списка репозиториев."""
    if not repos:
        return "> Нет релевантных DevOps-трендов за последние дни.\n"
    
    lines = [
        "| Репозиторий | Описание | Звёзды |",
        "|-------------|----------|--------|"
    ]
    for repo in repos:
        name = repo['name']
        url = repo['url']
        desc = (repo['description'] or "Без описания").replace("\n", " ")
        stars = repo['stars']
        lines.append(f"| [{name}]({url}) | {desc} | ⭐ {stars} |")
    return "\n".join(lines) + "\n"

def update_readme(trending_repos):
    """Обновляет секцию между <!-- TRENDS_START --> и <!-- TRENDS_END --> в README.md"""
    readme_path = os.path.join(os.path.dirname(__file__), "..", "README.md")
    
    # Читаем текущий README
    with open(readme_path, "r", encoding="utf-8") as f:
        content = f.read()

    start_marker = "<!-- TRENDS_START -->"
    end_marker = "<!-- TRENDS_END -->"

    if start_marker not in content or end_marker not in content:
        # Если маркеры отсутствуют — добавим их в конец
        table = generate_markdown_table(trending_repos)
        new_content = content.rstrip() + f"\n\n## 🏆 DevOps Trends (AI-analyzed)\n\n{start_marker}\n{table}{end_marker}\n"
    else:
        # Заменяем содержимое между маркерами
        table = generate_markdown_table(trending_repos)
        start_idx = content.find(start_marker) + len(start_marker)
        end_idx = content.find(end_marker)
        new_content = content[:start_idx] + "\n" + table + "\n" + content[end_idx:]

    # Записываем обновлённый README
    with open(readme_path, "w", encoding=" utf-8") as f:
        f.write(new_content)