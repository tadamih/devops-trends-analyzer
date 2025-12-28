# scripts/vector_search.py
"""
Простой семантический поиск на основе TF-IDF и косинусного сходства.
Не требует нейросетей — работает на scikit-learn.
"""

import os
import sys
sys.path.append(os.path.dirname(__file__))

from db import get_db_connection
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import numpy as np

QUERY_TEXT = "devops automation ci/cd kubernetes terraform infrastructure as code deployment monitoring"

def get_trending_repos(limit=5):
    """
    Возвращает топ репозиториев, наиболее похожих на QUERY_TEXT.
    Использует TF-IDF + косинусное сходство.
    """
    # 1. Получаем данные из БД
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute("SELECT name, description, url, stars FROM repos;")
    rows = cur.fetchall()
    cur.close()
    conn.close()

    if not rows:
        return []

    # 2. Подготавливаем тексты
    repo_data = []
    texts = []
    for name, desc, url, stars in rows:
        desc = desc or ""
        text = f"{name} {desc}".lower()
        if len(text.strip()) < 5:
            continue
        repo_data.append({"name": name, "description": desc, "url": url, "stars": stars})
        texts.append(text)

    if not texts:
        return []

    # 3. Векторизуем с помощью TF-IDF
    vectorizer = TfidfVectorizer(stop_words='english', ngram_range=(1, 2))
    tfidf_matrix = vectorizer.fit_transform([QUERY_TEXT] + texts)
    
    # 4. Считаем схожесть запроса с каждым репозиторием
    query_vec = tfidf_matrix[0:1]
    repo_vecs = tfidf_matrix[1:]
    similarities = cosine_similarity(query_vec, repo_vecs)[0]
    
    # 5. Сортируем
    ranked = sorted(
        zip(repo_data, similarities),
        key=lambda x: x[1],
        reverse=True
    )
    
    return [item[0] for item in ranked[:limit]]