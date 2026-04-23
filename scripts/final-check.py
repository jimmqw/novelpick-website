import re
import os

def fix_em_dash_entities(filepath):
    """Replace em-dash and bullet HTML entities with actual characters."""
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()
    
    original = content
    # Replace em-dash entity &#8212; with actual em-dash
    content = content.replace('&#8212;', '—')
    # Replace bullet entity &#9679; with actual bullet
    content = content.replace('&#9679;', '●')
    
    if content != original:
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(content)
        return True
    return False

# Fix fateandmethod files with em-dash entities
files_to_fix = [
    r'C:\Users\Administrator\.openclaw\workspace\fateandmethod.com\chinese-zodiac-compatibility-guide.html',
]

for f in files_to_fix:
    if os.path.exists(f):
        result = fix_em_dash_entities(f)
        fname = os.path.basename(f)
        print(f"{fname}: {'Fixed em-dash & bullet entities' if result else 'No change'}")

# Re-check all HTML files for remaining issues
def full_check(filepath):
    issues = []
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Em-dash entity
    if '&#8212;' in content:
        issues.append("EM_DASH_ENTITY: still has em-dash HTML entities")
    
    # Bullet entity
    if '&#9679;' in content:
        issues.append("BULLET_ENTITY: still has bullet HTML entities")
    
    # AI language
    ai_phrases = [('unmatched', r'\bunmatched\b'), ('cutting-edge', r'\bcutting-edge\b'), 
                  ('game-changing', r'\bgame-changing\b'), ('second-to-none', r'\bsecond-to-none\b'),
                  ('revolutionize', r'\brevolutionize\b'), ('best-in-class.*best-in-class', r'best-in-class.*best-in-class')]
    for phrase, pattern in ai_phrases:
        matches = re.findall(pattern, content, re.IGNORECASE)
        if matches:
            issues.append(f"AI_LANGUAGE: '{phrase}'")
    
    # BOM check
    with open(filepath, 'rb') as f:
        raw = f.read()
    if raw.startswith(b'\xef\xbb\xbf'):
        issues.append("BOM: has UTF-8 BOM")
    
    return issues

# Check all sites
sites = {
    'morai.top': r'C:\Users\Administrator\.openclaw\workspace\morai.top',
    'novelpick.top': r'C:\Users\Administrator\.openclaw\workspace\novelpick.top',
    'fateandmethod.com': r'C:\Users\Administrator\.openclaw\workspace\fateandmethod.com',
}

total_issues = 0
for site, path in sites.items():
    print(f"\n=== {site} ===")
    site_issues = 0
    for fname in sorted(os.listdir(path)):
        if fname.endswith('.html'):
            fpath = os.path.join(path, fname)
            issues = full_check(fpath)
            if issues:
                print(f"  {fname}:")
                for i in issues:
                    print(f"    - {i}")
                site_issues += len(issues)
    total_issues += site_issues
    print(f"  Total issues: {site_issues}")

print(f"\n=== TOTAL REMAINING ISSUES: {total_issues} ===")