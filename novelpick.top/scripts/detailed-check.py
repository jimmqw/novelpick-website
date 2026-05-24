import re
import os

def check_file_detailed(filepath):
    issues = []
    filename = os.path.basename(filepath)
    
    with open(filepath, 'rb') as f:
        raw = f.read()
    
    # Try decoding as UTF-8
    try:
        content = raw.decode('utf-8')
        encoding = 'utf-8'
    except UnicodeDecodeError as e:
        issues.append(f"ENCODING_ERROR: cannot decode as UTF-8 at position {e.start}")
        content = raw.decode('latin-1')
        encoding = 'latin-1 (fallback)'
    
    # Check for BOM
    if raw.startswith(b'\xef\xbb\xbf'):
        issues.append("BOM: file has UTF-8 BOM marker")
    
    # Check for em-dash entity
    em_dash_entities = re.findall(r'&#8212;', content)
    if em_dash_entities:
        issues.append(f"EM_DASH_ENTITY: found {len(em_dash_entities)} HTML entity for em-dash")
    
    # Check for bullet entity
    bullet_entities = re.findall(r'&#9679;', content)
    if bullet_entities:
        issues.append(f"BULLET_ENTITY: found {len(bullet_entities)} HTML entity for bullet")
    
    # Check div balance - find article-body section
    ab_start = content.find('<div class="article-body"')
    if ab_start < 0:
        ab_start = content.find('<div class=\"article-body\"')
    
    if ab_start >= 0:
        # Find next section boundary (prev-next, sidebar, or </main>)
        candidates = []
        for marker in ['<div class="prev-next"', '<aside', '</main>', '<div class="sidebar"']:
            pos = content.find(marker, ab_start + 1)
            if pos >= 0:
                candidates.append(pos)
        
        if candidates:
            boundary = min(candidates)
            article_content = content[ab_start + len('<div class="article-body"'):boundary]
            opens = article_content.count('<div')
            closes = article_content.count('</div>')
            diff = opens - closes
            if diff != 0:
                issues.append(f"DIV_UNBALANCED: article-body {opens} opens vs {closes} closes (diff={diff})")
        else:
            issues.append("DIV_CHECK_INCONCLUSIVE: could not find boundary after article-body")
    
    # AI language
    ai_phrases = [
        ('unmatched', r'\bunmatched\b'),
        ('cutting-edge', r'\bcutting-edge\b'),
        ('game-changing', r'\bgame-changing\b'),
    ]
    for phrase, pattern in ai_phrases:
        matches = re.findall(pattern, content, re.IGNORECASE)
        if matches:
            issues.append(f"AI_LANGUAGE: '{phrase}' found {len(matches)}x")
    
    return issues, encoding

# Check all fateandmethod HTML files
results = []
for fname in sorted(os.listdir(r'C:\Users\Administrator\.openclaw\workspace\fateandmethod.com')):
    if fname.endswith('.html'):
        fpath = os.path.join(r'C:\Users\Administrator\.openclaw\workspace\fateandmethod.com', fname)
        issues, enc = check_file_detailed(fpath)
        if issues:
            results.append((fname, enc, issues))

print(f"Files with issues: {len(results)}")
for fname, enc, issues in results:
    print(f"\n{fname} [{enc}]:")
    for i in issues:
        print(f"  - {i}")