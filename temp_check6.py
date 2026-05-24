import re

content = open(r'C:\Users\Administrator\github\fateandmethod-site\bazi.html', 'r', encoding='utf-8', errors='replace').read()

# Find article-body div
ab_pos = content.find('<div class="article-body">')
print('article-body div at:', ab_pos)

# Find closing </div> positions after it
search = content[ab_pos+20:]
div_positions = []
idx = 0
while True:
    idx = search.find('</div>', idx)
    if idx < 0:
        break
    div_positions.append(ab_pos + 20 + idx)
    idx += 6

print('First 10 </div> positions after article-body:', div_positions[:10])
print('Total </div> in segment:', len(div_positions))

# Find footer
footer_pos = content.find('<footer')
print('footer at:', footer_pos)

# Find recommended div
rec_pos = content.find('<div class="recommended"')
print('recommended at:', rec_pos)

# Extract text between article-body and footer/recommended
end_pos = footer_pos if footer_pos > 0 else len(content)
if rec_pos > 0:
    end_pos = min(end_pos, rec_pos)

segment = content[ab_pos:end_pos]
text = re.sub(r'<[^>]+>', '', segment).strip()
print('Text length:', len(text))
print('First 200 chars:', text[:200])