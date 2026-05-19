import re
f=open(r'C:\Users\Administrator\github\novelpick-website\romance.html','r',encoding='utf-8')
html=f.read()
f.close()
body=re.search(r'<div class="article-body"(?:[^>]*)>(.*?)</div>\s*<(?:aside|main|div class="related")',html,re.DOTALL)
print('Body found:', body is not None)
if body:
    text=re.sub(r'<[^>]+>',' ',body.group(1))
    text=text.replace('&nbsp;',' ').replace('&amp;','&')
    clean=' '.join(text.split())
    print('Text chars:', len(clean))
    print('Preview:', clean[:200])