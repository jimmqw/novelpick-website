# -*- coding: utf-8 -*-
import re

fpath = r"C:\Users\Administrator\github\morai-website\ai-agent-tools-2026.html"
with open(fpath, 'r', encoding='utf-8', errors='replace') as f:
    c = f.read()

# Find main content area
# Look for divs with specific classes
divs = re.findall(r'<div[^>]*class=["\']([^"\']+)["\'][^>]*>', c, re.IGNORECASE)
print("Div classes found:")
for cls in divs[:50]:
    print(f"  {cls}")

print("\n--- Looking for article/content areas ---")
content_divs = re.findall(r'<div[^>]*class=["\'][^"\']*(article|content|post|main)[^"\']*["\'][^>]*>', c, re.IGNORECASE)
print("Content-like divs:", content_divs[:20])

# body text
body_match = re.search(r'<body[^>]*>(.*?)</body>', c, re.DOTALL | re.IGNORECASE)
if body_match:
    text = re.sub(r'<[^>]+>', '', body_match.group(1))
    text = re.sub(r'\s+', '', text)
    print(f"\nBody text length: {len(text)}")
    print(f"First 500 chars of text: {text[:500]}")
