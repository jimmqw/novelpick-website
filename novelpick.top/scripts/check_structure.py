#!/usr/bin/env python3
import re

for site, fname in [
    ('morai', r'C:\Users\Administrator\.openclaw\workspace\morai-website\best-ai-agents-2026.html'),
    ('novelpick', r'C:\Users\Administrator\.openclaw\workspace\novelpick-website\best-action-fantasy-web-novels-2026.html'),
]:
    content = open(fname, encoding='utf-8').read()
    print(f'=== {site} ===')
    print(f'head: {content.count("<head>")}/{content.count("</head>")}')
    print(f'body: {content.count("<body>")}/{content.count("</body>")}')
    print(f'charset: {content.count("charset")}, viewport: {content.count("viewport")}')
    print(f'og:title: {content.count("og:title")}')
    body_start = content.find('<body>')
    print(f'scripts in body: {content[body_start:].count("<script")}')
    print(f'progress: {"progress" in content}')
    print(f'article-container: {"article-container" in content}')
    print(f'share-bar: {"share-bar" in content}')
    print(f'novel-card: {"novel-card" in content}')
    print(f'tool-card: {"tool-card" in content}')
    print()
