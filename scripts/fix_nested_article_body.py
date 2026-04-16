"""Remove duplicate/inner article-body div wrappers from novelpick articles"""
import re
import os

def fix_nested_article_body(filepath):
    with open(filepath, encoding='utf-8') as f:
        content = f.read()
    
    # Find all article-body opening tags
    pattern = re.compile(r'<div class="article-body">', re.IGNORECASE)
    matches = list(pattern.finditer(content))
    
    if len(matches) < 2:
        return False
    
    # Find all closing tags
    close_pattern = re.compile(r'</div>', re.IGNORECASE)
    closes = list(close_pattern.finditer(content))
    
    # We need to find the inner pair (the second opening tag and its closing tag)
    # Strategy: find the second <div class="article-body">, then find its matching </div>
    # by tracking nesting depth from that point
    second_open_start = matches[1].start()
    second_open_end = matches[1].end()
    
    depth = 1
    pos = second_open_end
    second_close = None
    
    while pos < len(content) and depth > 0:
        next_open = content.find('<div', pos)
        next_close = content.find('</div>', pos)
        
        if next_close < 0:
            break
        
        if next_open >= 0 and next_open < next_close:
            depth += 1
            pos = next_open + 5
        else:
            depth -= 1
            if depth == 0:
                second_close = next_close + 6
                break
            pos = next_close + 6
    
    if second_close is None:
        return False
    
    # Remove the inner article-body wrapper (opening tag, whitespace, and closing tag)
    # But keep the content inside
    inner_wrapper_start = matches[1].start()
    
    # What's between the inner opening and its close
    inner_content = content[second_open_end:second_close]
    
    new_content = content[:inner_wrapper_start] + inner_content + content[second_close:]
    
    if new_content != content:
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(new_content)
        return True
    return False

# Process all novelpick article files
path = r'C:\Users\Administrator\github\novelpick-website'
fixed = []
for f in os.listdir(path):
    if f.endswith('.html'):
        filepath = os.path.join(path, f)
        try:
            if fix_nested_article_body(filepath):
                fixed.append(f)
        except Exception as e:
            print(f"ERROR {f}: {e}")

print(f"Fixed {len(fixed)} files:")
for f in fixed:
    print(f"  {f}")
