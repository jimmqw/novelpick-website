import re
h = open(r'C:\Users\Administrator\github\fateandmethod-site\index.html','r',encoding='utf-8').read()
print('nav div:', bool(re.search(r'<div[^>]*class=["\'][^"\']*nav[^"\']*["\']', h)))
print('gradient:', bool(re.search(r'gradient', h)))
print('.nav CSS:', bool(re.search(r'\.nav\s*\{', h)))
# Check for breadcrumb
print('breadcrumb:', bool(re.search(r'breadcrumb', h, re.IGNORECASE)))
# Check for footer
print('footer div:', bool(re.search(r'class=["\'][^"\']*footer[^"\']*["\']', h)))
print('footer tag:', bool(re.search(r'<footer', h)))
