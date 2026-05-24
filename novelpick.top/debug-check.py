import re

# Test check_header function
def check_header(html: str) -> bool:
    """Check if header/nav exists with dark gradient background"""
    has_nav_tag = bool(re.search(r'<nav[^>]*>', html, re.IGNORECASE))
    has_header_tag = bool(re.search(r'<header[^>]*>', html, re.IGNORECASE))
    has_gradient = bool(re.search(r'gradient|linear-gradient', html, re.IGNORECASE))
    return (has_nav_tag or has_header_tag) and has_gradient

h = open(r'C:\Users\Administrator\github\novelpick-website\best-action-fantasy-web-novels-2026.html','r',encoding='utf-8').read()
print('nav tag:', bool(re.search(r'<nav[^>]*>', h)))
print('header tag:', bool(re.search(r'<header[^>]*>', h)))
print('gradient:', bool(re.search(r'gradient|linear-gradient', h)))
print('check_header result:', check_header(h))
