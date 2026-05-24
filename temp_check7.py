import re

content = open(r'C:\Users\Administrator\github\fateandmethod-site\bazi.html', 'r', encoding='utf-8', errors='replace').read()

# The issue: my pattern stops at first </div> after article-body opening
# My pattern: r'<div[^>]*\bclass=["\']([^"\']*\barticle-body\b[^"\']*)["\'][^>]*>(.*?)</div>\s*(?=</article|\n\s*<footer|<div class="recommended|<div class="keep)'
# The problem: the content has nested divs. The (.*?) matches the first </div> it finds, not the one that closes article-body.

# Instead, we should:
# 1. Find the opening <div class="article-body"> position
# 2. Search from there until we hit the next major section (footer or recommended or similar)

ab_pos = content.find('<div class="article-body">')
if ab_pos < 0:
    print("No article-body div found")
    exit()

# Find the next </footer> or <div class="recommended" after the article-body
footer_pos = content.find('<footer', ab_pos)
rec_pos = content.find('<div class="recommended"', ab_pos)

end_pos = len(content)
if footer_pos > 0:
    end_pos = footer_pos
if rec_pos > 0 and rec_pos < end_pos:
    end_pos = rec_pos

# Extract article content
article_content = content[ab_pos:end_pos]
text = re.sub(r'<[^>]+>', '', article_content).strip()
print(f"Text length: {len(text)}")
print(f"Preview: {text[:200]}")

# Now let's see what my get_article_text function was actually doing wrong
# My function tried: r'<div[^>]*\bclass=["\'][^"\']*\barticle-body\b[^"\']*["\'][^>]*>(.*?)</div>'
# This is a non-greedy match that stops at the FIRST </div>

# The fix: don't match (.*?) against </div>, instead find the article-body div boundary and extract until footer/recommended