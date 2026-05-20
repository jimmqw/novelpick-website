with open(r'C:\Users\Administrator\github\novelpick-website\scifi.html', 'r', encoding='utf-8') as f:
    content = f.read()

# Find the section between article-body close and related div
article_body_close_pos = 10421  # This is the </div> that closes article-body
# The next </div> is the orphaned one at 10432
# But we need to look at content from 10432 to related (19588)
orphaned_segment = content[10432:19588]
print('Length of orphaned segment:', len(orphaned_segment))
print('First 200 chars:', orphaned_segment[:200])
print()
# Check for </div> in that segment
count = orphaned_segment.count('</div>')
print('</div> count in orphaned segment:', count)

# Let's also check the original file to see what was there
# The problem: we need to see what divs are between article_body_close and related
# Let me look at what's actually in the file around line 197-202
lines = content.split('\n')
for i, line in enumerate(lines[193:205], start=194):
    print(f'{i}: {line}')