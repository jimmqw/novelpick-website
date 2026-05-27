import re
import os

def fix_html_entities(filepath):
    """Convert HTML emoji entities to actual emoji characters."""
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Map of common emoji HTML entities to actual emoji
    entity_map = {
        '&#128200;': '📈',
        '&#128260;': '🦋',
        '&#128157;': '💙',
        '&#9889;': '⚡',
        '&#128218;': '📚',
        '&#128193;': '📁',
        '&#128293;': '🔥',
        '&#128336;': '⏰',
        '&#128197;': '📅',
        '&#9201;': '⏱',
        '&#9998;': '✍',
        '&#8250;': '›',
    }
    
    original = content
    for entity, emoji in entity_map.items():
        content = content.replace(entity, emoji)
    
    if content != original:
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(content)
        return True
    return False

# Fix novelpick articles with HTML emoji entities
files_to_fix = [
    r'C:\Users\Administrator\.openclaw\workspace\novelpick.top\best-cultivation-novels-2026.html',
    r'C:\Users\Administrator\.openclaw\workspace\novelpick.top\best-reincarnation-web-novels-2026.html',
    r'C:\Users\Administrator\.openclaw\workspace\fateandmethod.com\chinese-zodiac-compatibility-guide.html',
]

for f in files_to_fix:
    if os.path.exists(f):
        result = fix_html_entities(f)
        print(f"{os.path.basename(f)}: {'Fixed' if result else 'No change'}")

# Check AI language patterns and fix them
def fix_ai_language(filepath):
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()
    
    replacements = {
        'unmatched': 'excellent',
        'cutting-edge': 'advanced',
        'game-changing': 'significant',
        'second-to-none': 'among the best',
    }
    
    original = content
    for phrase, replacement in replacements.items():
        content = re.sub(r'\b' + phrase + r'\b', replacement, content, flags=re.IGNORECASE)
    
    if content != original:
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(content)
        return True
    return False

ai_files = [
    r'C:\Users\Administrator\.openclaw\workspace\novelpick.top\best-cultivation-novels-2026.html',
    r'C:\Users\Administrator\.openclaw\workspace\novelpick.top\best-reincarnation-web-novels-2026.html',
    r'C:\Users\Administrator\.openclaw\workspace\novelpick.top\books-like-solo-leveling.html',
    r'C:\Users\Administrator\.openclaw\workspace\morai.top\best-ai-video-generation-tools-2026.html',
]

for f in ai_files:
    if os.path.exists(f):
        result = fix_ai_language(f)
        print(f"{os.path.basename(f)} AI language fix: {'Applied' if result else 'No change'}")

print('\nDone!')