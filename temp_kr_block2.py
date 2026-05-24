content = open(r'C:\Users\Administrator\github\novelpick-website\best-cultivation-novels-2026.html', 'r', encoding='utf-8', errors='replace').read()

# Check if Keep Reading already exists
if 'keep-reading' in content.lower() or 'related-articles' in content.lower():
    print('Keep Reading already exists')
else:
    print('Need to add Keep Reading block')
    
# Check if prev-next nav exists
prevnext = content.find('class="prev-next"')
print(f'prev-next at: {prevnext}')

# Keep Reading block to add
kr_block = '''
                <div class="related-articles">
                    <h3>Keep Reading</h3>
                    <div class="related-grid">
                        <a href="/best-reincarnation-web-novels-2026.html" class="related-card">
                            <span class="related-tag">Reincarnation</span>
                            <span class="related-title">Best Reincarnation Web Novels 2026</span>
                        </a>
                        <a href="/best-progression-fantasy-novels.html" class="related-card">
                            <span class="related-tag">Progression</span>
                            <span class="related-title">Best Progression Fantasy Novels</span>
                        </a>
                        <a href="/best-historical-fantasy-novels.html" class="related-card">
                            <span class="related-tag">Historical</span>
                            <span class="related-title">Best Historical Fantasy Novels</span>
                        </a>
                        <a href="/best-harem-fantasy-novels-2026.html" class="related-card">
                            <span class="related-tag">Harem</span>
                            <span class="related-title">Best Harem Fantasy Novels 2026</span>
                        </a>
                    </div>
                </div>
'''

insert_point = content.find('<nav class="prev-next">')
if insert_point >= 0:
    new_content = content[:insert_point] + kr_block + content[insert_point:]
    open(r'C:\Users\Administrator\github\novelpick-website\best-cultivation-novels-2026.html', 'w', 'utf-8').write(new_content)
    print('Done! Keep Reading block added.')
else:
    print('Could not find prev-next nav')
