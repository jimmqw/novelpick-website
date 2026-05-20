with open(r'C:\Users\Administrator\github\novelpick-website\scifi.html', 'r', encoding='utf-8') as f:
    content = f.read()

# Find the article-body open tag
body_start = content.find('<div class="article-body">')

# Find the end: the </div> that closes article-body is NOT the one right after body_start
# but the one that comes right before <div class="related">
# article-body structure: <div class="article-body">...content...</div>
# related comes AFTER article-body closes

# Strategy: find <div class="related"> and look backwards for </div>
related_pos = content.find('<div class="related">')
# The </div> right before <div class="related"> is the article-body close
body_close = content.rfind('</div>', 0, related_pos)
print('article-body closes at byte:', body_close)
print('related div at byte:', related_pos)

# Also find sidebar
sidebar_pos = content.find('<aside class="sidebar">')
print('sidebar at byte:', sidebar_pos)

# Show what's between body_close and related
between = content[body_close:related_pos+200]
print()
print('Between body_close and related (first 300 bytes):')
try:
    print(between[:300].decode('utf-8', errors='replace'))
except:
    print('--- could not print ---')
    
# Count what's in the article-body
body_content = content[body_start:body_close+6]
print()
print('Article-body content length:', len(body_content))
print('Open divs:', body_content.count('<div '))
print('Close divs:', body_content.count('</div>'))