content = open(r'C:\Users\Administrator\github\fateandmethod-site\daily-wisdom.html', 'r', encoding='utf-8', errors='replace').read()
import re

sections = re.findall(r'<section[^>]*class="([^"]+)"', content)
print('Sections:', sections)

related = re.search(r'class="([^"]*related[^"]*)"', content, re.IGNORECASE)
print('Related:', related.group(1) if related else 'None')

footer = content.find('<footer')
print('Footer at:', footer)
print('Before footer:', repr(content[footer-300:footer]))
