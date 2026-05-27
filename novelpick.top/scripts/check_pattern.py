import re

path = r'C:\Users\Administrator\github\novelpick-website\best-solo-leveling-novels.html'
c = open(path, encoding='utf-8').read()

# Find the exact pattern between article-body and article-header
idx_ab = c.find('<div class="article-body">')
if idx_ab >= 0:
    start = idx_ab
    end = start + 100
    print('Around article-body:')
    print(repr(c[start:end]))
    idx_ah = c.find('<div class="article-header">')
    print(f'article-header at: {idx_ah}')
    if idx_ah >= 0:
        print('Around article-header:')
        print(repr(c[idx_ah-50:idx_ah+50]))
