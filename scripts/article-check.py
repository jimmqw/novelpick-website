import re
import os
from html.parser import HTMLParser

class DivCounter(HTMLParser):
    def __init__(self):
        super().__init__()
        self.open_divs = 0
        self.max_depth = 0
        self.current_depth = 0
        self.in_article_body = False
        
    def handle_starttag(self, tag, attrs):
        if tag == 'div':
            attrs_dict = dict(attrs)
            if self.in_article_body:
                self.open_divs += 1
                self.current_depth += 1
                self.max_depth = max(self.max_depth, self.current_depth)
        # Check if we enter article-body
        for attr_name, attr_val in attrs:
            if attr_val and 'article-body' in str(attr_val):
                self.in_article_body = True
                
    def handle_endtag(self, tag):
        if tag == 'div' and self.in_article_body:
            self.open_divs -= 1
            self.current_depth -= 1

def check_file(filepath):
    issues = []
    filename = os.path.basename(filepath)
    
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # 1. Garbled chars check
    garbled_patterns = [
        r'鈥橝',  # em-dash garbled
        r'锛?',   # Chinese punctuation garbled
    ]
    for pattern in garbled_patterns:
        if re.search(pattern, content):
            issues.append(f"GARBLED_CHAR: found garbled char matching {pattern}")
    
    # 2. Emoji entities vs actual emoji
    emoji_entities = re.findall(r'&#\d+;', content)
    if len(emoji_entities) > 5:
        issues.append(f"EMOJI_ENTITIES: {len(emoji_entities)} emoji HTML entities (should use actual emoji)")
    
    # 3. Check for AI language patterns
    ai_phrases = [
        r'remarkably\s+impressive',
        r'game-changing',
        r'unmatched',
        r'unparalleled',
        r'stands\s+head\s+and\s+shoulders',
        r'second\s+to\s+none',
        r'unrivaled',
        r'cutting-edge',
        r'without\s+a\s+doubt',
        r'trimumph\s+of\s+',
        r'revolutionize',
        r'game changer',
        r'best-in-class.*best-in-class',
    ]
    for phrase in ai_phrases:
        matches = re.findall(phrase, content, re.IGNORECASE)
        if matches:
            issues.append(f"AI_LANGUAGE: found '{matches[0]}' ({len(matches)} occurrences)")
    
    # 4. Check div balance in article-body
    article_body_match = re.search(r'<div[^>]*class="[^"]*article-body[^"]*"[^>]*>(.*?)</div>\s*(?=<div|</main|<aside|<footer)', content, re.DOTALL)
    if article_body_match:
        article_content = article_body_match.group(1)
        div_count = article_content.count('<div') - article_content.count('</div')
        if div_count != 0:
            issues.append(f"DIV_UNBALANCED: article-body has {div_count} unclosed divs (open - close)")
    
    # 5. Check internal links
    site_name = None
    if 'novelpick' in filepath:
        site_name = 'novelpick.top'
    elif 'morai' in filepath:
        site_name = 'morai.top'
    elif 'fateandmethod' in filepath:
        site_name = 'fateandmethod.com'
    
    if site_name:
        internal_links = re.findall(r'href="(/[^"]*)"', content)
        for link in internal_links:
            if link.startswith('/') and not link.startswith(f'/{site_name.split(".")[0]}'):
                # Might be broken
                pass
    
    # 6. Check date freshness
    date_patterns = [
        r'(January|February|March|April|May|June|July|August|September|October|November|December)\s+\d{1,2},\s+202[4-5]',
        r'20\d{2}-\d{2}-\d{2}',
    ]
    for pattern in date_patterns:
        matches = re.findall(pattern, content)
        if matches:
            for match in matches:
                # Check if year is 2024 or earlier
                year_match = re.search(r'202[0-4]', match)
                if year_match:
                    issues.append(f"STALE_DATE: found date '{match}' from {year_match.group()}")
    
    # 7. Check for empty/bare paragraphs
    bare_p_count = len(re.findall(r'<p>\s*</p>', content))
    if bare_p_count > 0:
        issues.append(f"EMPTY_PARAGRAPHS: {bare_p_count} empty <p> tags")
    
    return issues

def scan_directory(dirpath, limit=None):
    results = []
    count = 0
    for root, dirs, files in os.walk(dirpath):
        for file in files:
            if file.endswith('.html'):
                filepath = os.path.join(root, file)
                issues = check_file(filepath)
                if issues:
                    results.append((filepath, issues))
                count += 1
                if limit and count >= limit:
                    break
    return results

# Scan all three sites
all_results = []

sites = {
    'morai.top': r'C:\Users\Administrator\.openclaw\workspace\morai.top',
    'novelpick.top': r'C:\Users\Administrator\.openclaw\workspace\novelpick.top',
    'fateandmethod.com': r'C:\Users\Administrator\.openclaw\workspace\fateandmethod.com',
}

for site, path in sites.items():
    print(f"\n=== {site} ===")
    results = scan_directory(path)
    for filepath, issues in results:
        print(f"\n{os.path.basename(filepath)}:")
        for issue in issues:
            print(f"  - {issue}")
    all_results.extend(results)

print(f"\n\n=== SUMMARY ===")
print(f"Files scanned: 3")
print(f"Files with issues: {len(all_results)}")
for site, path in sites.items():
    site_results = [r for r in all_results if site in r[0]]
    print(f"{site}: {len(site_results)} files with issues")