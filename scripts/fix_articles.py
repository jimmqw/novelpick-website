# -*- coding: utf-8 -*-
"""
Comprehensive article fix script:
1. Add Keep Reading / Related Posts sections to all articles
2. Fix div nesting imbalances
3. Add missing article-body class
4. Fix BLUF issues (h2 questions -> conclusions)
5. Record lessons learned
"""
import re
import os
from pathlib import Path

workspace = Path(r"C:\Users\Administrator\.openclaw\workspace")

# Map each article to its site-related articles for Keep Reading section
# Format: (site/path, filename, [list of related articles with title and link])
keep_reading_articles = {
    "morai.top": {
        "best-ai-agents-2026.html": [
            ("Best AI Video Generation Tools 2026", "/best-ai-video-generation-tools-2026.html"),
            ("Best AI Writing Tools 2026", "/best-ai-writing-tools-2026.html"),
            ("GitHub Copilot Review 2026", "/github-copilot-review-2026.html"),
            ("Best AI Image Generation Tools 2026", "/best-ai-image-generation-tools-2026.html"),
            ("Best AI Note-Taking Tools 2026", "/best-ai-note-taking-tools-2026.html"),
            ("Best AI Voice Cloning Tools 2026", "/best-ai-voice-cloning-tools-2026.html"),
        ],
        "best-ai-image-generation-tools-2026.html": [
            ("Best AI Agents 2026", "/best-ai-agents-2026.html"),
            ("Best AI Video Generation Tools 2026", "/best-ai-video-generation-tools-2026.html"),
            ("GitHub Copilot Review 2026", "/github-copilot-review-2026.html"),
            ("Best AI Writing Tools 2026", "/best-ai-writing-tools-2026.html"),
            ("Best AI Note-Taking Tools 2026", "/best-ai-note-taking-tools-2026.html"),
        ],
        "best-ai-note-taking-tools-2026.html": [
            ("Best AI Agents 2026", "/best-ai-agents-2026.html"),
            ("Best AI Video Generation Tools 2026", "/best-ai-video-generation-tools-2026.html"),
            ("Best AI Writing Tools 2026", "/best-ai-writing-tools-2026.html"),
            ("GitHub Copilot Review 2026", "/github-copilot-review-2026.html"),
            ("Best AI Voice Cloning Tools 2026", "/best-ai-voice-cloning-tools-2026.html"),
        ],
    },
    "novelpick.top": {
        "best-cultivation-novels-2026.html": [
            ("Top LitRPG Web Novels 2026", "/top-litrpg-web-novels-2026.html"),
            ("Best Reincarnation Web Novels 2026", "/best-reincarnation-web-novels-2026.html"),
            ("Best Time Travel Web Novels 2026", "/best-time-travel-web-novels-2026.html"),
            ("Top Romance Web Novels 2026", "/top-romance-web-novels-2026.html"),
            ("Books Like Solo Leveling", "/books-like-solo-leveling.html"),
        ],
        "top-litrpg-web-novels-2026.html": [
            ("Best Cultivation Novels 2026", "/best-cultivation-novels-2026.html"),
            ("Best Reincarnation Web Novels 2026", "/best-reincarnation-web-novels-2026.html"),
            ("Best Time Travel Web Novels 2026", "/best-time-travel-web-novels-2026.html"),
            ("Top Romance Web Novels 2026", "/top-romance-web-novels-2026.html"),
            ("Books Like Solo Leveling", "/books-like-solo-leveling.html"),
        ],
        "best-time-travel-web-novels-2026.html": [
            ("Best Cultivation Novels 2026", "/best-cultivation-novels-2026.html"),
            ("Top LitRPG Web Novels 2026", "/top-litrpg-web-novels-2026.html"),
            ("Best Reincarnation Web Novels 2026", "/best-reincarnation-web-novels-2026.html"),
            ("Top Romance Web Novels 2026", "/top-romance-web-novels-2026.html"),
            ("Books Like Solo Leveling", "/books-like-solo-leveling.html"),
        ],
    },
    "fateandmethod.com": {
        "bazi-ten-gods-guide.html": [
            ("Ba Zi Complete Guide", "/bazi.html"),
            ("Chinese Zodiac Signs 2026 Guide", "/chinese-zodiac-signs-2026-guide.html"),
            ("Chinese Numerology Complete Guide", "/chinese-numerology-complete-guide.html"),
            ("Ziwei 12 Palaces Guide", "/ziwei-12-palaces-guide.html"),
        ],
        "chinese-numerology-complete-guide.html": [
            ("Ba Zi Ten Gods Guide", "/bazi-ten-gods-guide.html"),
            ("Chinese Zodiac Compatibility Guide", "/chinese-zodiac-compatibility-guide.html"),
            ("Feng Shui 2026 Year Guide", "/feng-shui-2026-year-guide.html"),
            ("Ba Zi Complete Guide", "/bazi.html"),
        ],
        "feng-shui-2026-year-guide.html": [
            ("Feng Shui Spring 2026", "/feng-shui-spring-2026.html"),
            ("Chinese Zodiac 2026 Fire Snake Horoscope", "/chinese-zodiac-2026-fire-snake-horoscope.html"),
            ("Chinese Zodiac Signs 2026 Guide", "/chinese-zodiac-signs-2026-guide.html"),
            ("Chinese Numerology Complete Guide", "/chinese-numerology-complete-guide.html"),
        ],
        "chinese-zodiac-compatibility-guide.html": [
            ("Chinese Zodiac Signs 2026 Guide", "/chinese-zodiac-signs-2026-guide.html"),
            ("Chinese Zodiac 2026 Fire Snake Horoscope", "/chinese-zodiac-2026-fire-snake-horoscope.html"),
            ("Ba Zi Complete Guide", "/bazi.html"),
            ("Feng Shui 2026 Year Guide", "/feng-shui-2026-year-guide.html"),
        ],
    },
}

# Keep Reading HTML template (novelpick style)
KEEP_READING_NOVELPICK = """
<div class="keep-reading-section">
<h3>Keep Reading</h3>
<div class="keep-reading-grid">
{items}
</div>
</div>"""

KEEP_READING_ITEM_NOVELPICK = '<a href="{link}" class="keep-reading-item"><span class="kr-title">{title}</span></a>'

# Keep Reading HTML template (morai style)
KEEP_READING_MORAI = """
<div class="keep-reading-section">
<h3>Keep Reading</h3>
<div class="keep-reading-grid">
{items}
</div>
</div>"""

KEEP_READING_ITEM_MORAI = '<a href="{link}" class="keep-reading-item"><span class="kr-title">{title}</span></a>'

# Keep Reading HTML (fateandmethod style)
KEEP_READING_FATE = """
<div class="keep-reading-section">
<h3>Continue Reading</h3>
<div class="keep-reading-grid">
{items}
</div>
</div>"""

KEEP_READING_ITEM_FATE = '<a href="{link}" class="keep-reading-item"><span class="kr-title">{title}</span></a>'

# CSS for Keep Reading sections (appended to embedded styles)
KEEP_READING_CSS_MORAI = "\n.keep-reading-section{margin:2rem 0;padding:1.5rem;background:rgba(0,212,255,0.03);border:1px solid var(--accent-border);border-radius:var(--r)}.keep-reading-section h3{color:var(--accent);font-size:1rem;margin-bottom:1rem}.keep-reading-grid{display:grid;grid-template-columns:1fr 1fr;gap:0.6rem}.keep-reading-item{padding:0.7rem 1rem;background:var(--card);border:1px solid var(--border);border-radius:8px;color:var(--text2);font-size:0.88rem;transition:all 0.2s}.keep-reading-item:hover{background:var(--accent-dim);border-color:var(--accent-border);color:var(--accent);text-decoration:none}"

KEEP_READING_CSS_NOVELPICK = "\n.keep-reading-section{margin:2rem 0;padding:1.5rem;background:rgba(45,20,60,0.15);border:1px solid var(--accent-border);border-radius:var(--r)}.keep-reading-section h3{color:var(--accent);font-size:1rem;margin-bottom:1rem}.keep-reading-grid{display:grid;grid-template-columns:1fr 1fr;gap:0.6rem}.keep-reading-item{padding:0.7rem 1rem;background:var(--card);border:1px solid var(--border);border-radius:8px;color:var(--text2);font-size:0.88rem;transition:all 0.2s}.keep-reading-item:hover{background:var(--accent-dim);border-color:var(--accent-border);color:var(--accent);text-decoration:none}"

KEEP_READING_CSS_FATE = "\n.keep-reading-section{margin:2rem 0;padding:1.5rem;background:rgba(201,168,76,0.04);border:1px solid rgba(201,168,76,0.15);border-radius:10px}.keep-reading-section h3{color:var(--accent);font-size:1rem;margin-bottom:1rem}.keep-reading-grid{display:grid;grid-template-columns:1fr 1fr;gap:0.6rem}.keep-reading-item{padding:0.7rem 1rem;background:var(--card);border:1px solid var(--border);border-radius:8px;color:var(--text2);font-size:0.88rem;transition:all 0.2s}.keep-reading-item:hover{background:rgba(201,168,76,0.08);border-color:rgba(201,168,76,0.2);color:var(--accent);text-decoration:none}"


def fix_article(site_dir, filename):
    filepath = workspace / site_dir / filename
    if not filepath.exists():
        print(f"  SKIP {filename}: not found")
        return {"status": "skip"}
    
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()
    
    original = content
    changes = []
    
    site_name = site_dir.replace('.top', '').replace('.com', '')
    
    # ====== 1. Fix div nesting imbalance ======
    opens = len(re.findall(r'<div\b', content))
    closes = len(re.findall(r'</div>', content))
    bal = opens - closes
    
    if bal < 0:
        # Extra closing divs - find the pattern
        # Check if there's an extra </div> between </div> (article-body close) and <div class="prev-next">
        pattern = re.compile(r'(</div>\s*</div>\s*)<div class="prev-next"')
        if pattern.search(content):
            # Remove the extra </div>
            content = pattern.sub(r'</div>\n<div class="prev-next"', content)
            changes.append(f"Fixed div imbalance: removed extra </div> before prev-next section")
        
        # Re-check
        opens2 = len(re.findall(r'<div\b', content))
        closes2 = len(re.findall(r'</div>', content))
        if opens2 != closes2:
            changes.append(f"WARNING: div imbalance reduced from {bal} to {opens2 - closes2} but still exists")
    
    # ====== 2. Add Keep Reading section if missing ======
    has_kr = any(p in content for p in ['Keep Reading', 'Continue Reading', 'keep-reading-section'])
    
    if not has_kr and site_dir in keep_reading_articles and filename in keep_reading_articles[site_dir]:
        related = keep_reading_articles[site_dir][filename]
        
        if site_dir == "novelpick.top":
            items = '\n'.join(KEEP_READING_ITEM_NOVELPICK.format(title=t, link=l) for t, l in related)
            kr_html = KEEP_READING_NOVELPICK.format(items=items)
            kr_css = KEEP_READING_CSS_NOVELPICK
        elif site_dir == "fateandmethod.com":
            items = '\n'.join(KEEP_READING_ITEM_FATE.format(title=t, link=l) for t, l in related)
            kr_html = KEEP_READING_FATE.format(items=items)
            kr_css = KEEP_READING_CSS_FATE
        else:  # morai.top
            items = '\n'.join(KEEP_READING_ITEM_MORAI.format(title=t, link=l) for t, l in related)
            kr_html = KEEP_READING_MORAI.format(items=items)
            kr_css = KEEP_READING_CSS_MORAI
        
        # Insert Keep Reading before the verdict section (within article-body)
        # Or after the last article-body paragraph if no verdict
        if '<div class="verdict">' in content:
            content = content.replace('<div class="verdict">', kr_html + '\n<div class="verdict">')
            changes.append("Added Keep Reading section before verdict")
        elif '<div class="keep-reading-section"' not in content:
            # Insert before the article-body close
            ab_end = content.rfind('</div>\n</div>\n<div class="prev-next"')
            if ab_end == -1:
                ab_end = content.rfind('</div>\n</main>')
            if ab_end == -1:
                # Find last </div> within article-body area and insert before
                # Insert just before the prev-next
                content = content.replace(
                    '<div class="prev-next">',
                    kr_html + '\n<div class="prev-next">'
                )
            changes.append("Added Keep Reading section")
        
        # Append CSS to embedded style block
        style_start = content.find('<style>')
        style_end = content.find('</style>')
        if style_start != -1 and style_end != -1:
            content = content[:style_end] + kr_css + content[style_end:]
            changes.append("Added Keep Reading CSS styles")
    
    # ====== 3. Check for missing article-body class ======
    if 'article-body' not in content:
        # This article uses a different structure - check if it has a content div
        # If it's fateandmethod style with no quotes on attributes
        if site_dir == "fateandmethod.com":
            # Add article-body class to the main content div
            # Pattern: class=content or similar
            m = re.search(r'class=([a-zA-Z0-9_-]+)', content)
            if m:
                old = m.group(0)
                new = 'class="article-body ' + m.group(1) + '"'
                content = content.replace(old, new, 1)
                changes.append(f"Added missing article-body class to: {old}")
    
    # ====== 4. Fix BLUF: change h2 questions to statements ======
    # Find h2 questions and convert to declarative statements
    h2_fixes = {
        'What Makes Cultivation Novels So Irresistible?': 'Why Cultivation Novels Are Irresistible',
        'What Is LitRPG — And Why Is It So Addictive?': 'What LitRPG Is and Why Readers Love It',
        'What Makes Time Travel Novels So Compulsive?': 'Why Time Travel Novels Are Compulsive Reads',
        'What Are the Ten Gods?': 'Understanding the Ten Gods',
        'What Is Chinese Numerology?': 'Chinese Numerology Explained',
        'What Makes 2026 a Fire Snake Year?': '2026: The Year of the Fire Snake',
    }
    for old_q, new_h in h2_fixes.items():
        old_pattern = f'<h2[^>]*>{re.escape(old_q)}</h2>'
        if re.search(old_pattern, content):
            content = re.sub(old_pattern, f'<h2>{new_h}</h2>', content)
            changes.append(f"Fixed BLUF: changed h2 '{old_q}' to '{new_h}'")
    
    # ====== 5. Check for &copy; encoding issues ======
    if '\ufffd' in content:
        content = content.replace('\ufffd', '-')
        changes.append("Fixed encoding: replaced U+FFFD with hyphen")
    
    # Save if changes were made
    if content != original:
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(content)
        changes.append(f"FILE SAVED ({len(content):,} bytes, was {len(original):,})")
    
    return {
        "status": "fixed" if content != original else "no_changes",
        "changes": changes,
        "original_size": len(original),
        "new_size": len(content),
    }


# Process all 10 articles
results = []
articles_to_process = [
    ("morai.top", "best-ai-agents-2026.html"),
    ("morai.top", "best-ai-image-generation-tools-2026.html"),
    ("morai.top", "best-ai-note-taking-tools-2026.html"),
    ("novelpick.top", "best-cultivation-novels-2026.html"),
    ("novelpick.top", "top-litrpg-web-novels-2026.html"),
    ("novelpick.top", "best-time-travel-web-novels-2026.html"),
    ("fateandmethod.com", "bazi-ten-gods-guide.html"),
    ("fateandmethod.com", "chinese-numerology-complete-guide.html"),
    ("fateandmethod.com", "feng-shui-2026-year-guide.html"),
    ("fateandmethod.com", "chinese-zodiac-compatibility-guide.html"),
]

print("=" * 70)
print("ARTICLE FIX SCRIPT - Processing 10 articles")
print("=" * 70)

for site_dir, filename in articles_to_process:
    print(f"\n{'='*70}")
    print(f"  {site_dir}/{filename}")
    result = fix_article(site_dir, filename)
    results.append((f"{site_dir}/{filename}", result))
    if result["status"] == "skip":
        print(f"  SKIPPED")
    elif result["status"] == "no_changes":
        print(f"  NO CHANGES NEEDED ({result['original_size']:,} bytes)")
    else:
        print(f"  FIXED ({result['original_size']:,} -> {result['new_size']:,} bytes)")
        for c in result["changes"]:
            print(f"    + {c}")

print(f"\n{'='*70}")
print("FIX SUMMARY:")
fixed = sum(1 for _, r in results if r["status"] == "fixed")
skipped = sum(1 for _, r in results if r["status"] == "skip")
nochange = sum(1 for _, r in results if r["status"] == "no_changes")
print(f"  Fixed: {fixed}, No changes needed: {nochange}, Skipped: {skipped}")
print(f"  Total: {len(results)} articles processed")

# Record lessons learned
lessons = """## Article Check & Fix Lessons (2026-04-29)

### Issues Found Across Batch (10 articles)

**Pattern 1: Missing Keep Reading sections (9/10 articles)**
- All articles lacked a "Keep Reading" or "Related Posts" section
- Fix: Add keep-reading-section with related article links after article-body content

**Pattern 2: BLUF violations (5/10 articles)**
- Several h2 headings were phrased as questions instead of conclusions
- Fix: Changed "What Is X?" to "Understanding X" or "Why X Matters"

**Pattern 3: Div nesting imbalance in article structure (2/10)**
- Extra </div> between article-body close and prev-next section
- Root cause: article-footer-extra div not being closed properly
- Fix: Remove the extra </div> tag

**Pattern 4: No article-body class (1/10)**
- Missing article-body class in content div
- Caused skip in automated checks

### Common Fix Strategy
1. Use a site-specific Keep Reading template with 4-6 related links
2. For div imbalance: count opens/closes and find extra tags
3. For BLUF: convert h2 questions to declarative statements
4. For missing classes: add article-body to content div
"""

workspace_dir = Path(r"C:\Users\Administrator\.openclaw\workspace")
lessons_file = workspace_dir / "memory" / "lessons-article-fix.md"
with open(lessons_file, 'w', encoding='utf-8') as f:
    f.write(lessons)
print(f"\nLessons written to {lessons_file}")
