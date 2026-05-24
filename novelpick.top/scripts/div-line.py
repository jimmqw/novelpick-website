with open(r'C:\Users\Administrator\.openclaw\workspace\morai.top\best-ai-agents-2026.html', 'r', encoding='utf-8') as f:
    lines = f.readlines()

in_article_body = False
depth = 0
found_end = False
for i, line in enumerate(lines):
    stripped = line.rstrip()
    if 'class="article-body"' in line:
        in_article_body = True
        depth = 1
        print(f'Line {i+1} [OPEN article-body, depth={depth}]: {stripped[:80]}')
    elif in_article_body:
        if stripped.startswith('<div'):
            depth += 1
            print(f'Line {i+1} [div open, depth={depth}]: {stripped[:80]}')
        elif '</div>' in stripped:
            # Check if this closes article-body
            if stripped.strip() == '</div>' and depth == 1:
                print(f'Line {i+1} [CLOSE article-body, depth={depth}]: {stripped[:80]}')
                in_article_body = False
                found_end = True
                break
            depth -= 1
            print(f'Line {i+1} [div close, depth={depth}]: {stripped[:80]}')

if not found_end:
    print(f'\n=== Did not find end! Final depth={depth} ===')
    # Print last 10 lines around where we think article-body should end
    print('Last 20 lines:')
    for j in range(max(0, len(lines)-20), len(lines)):
        print(f'  {j+1}: {lines[j].rstrip()[:100]}')