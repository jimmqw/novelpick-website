content = open(r'C:\Users\Administrator\github\novelpick-website\best-cultivation-novels-2026.html', 'r', encoding='utf-8', errors='replace').read()

# The Keep Reading block to add
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

# Find the insertion point: before <nav class="prev-next">
insert_point = content.find('<nav class="prev-next">')
print(f'Insert point (prev-next) at: {insert_point}')
print(f'Context: {repr(content[insert_point-50:insert_point+30])}')

# Insert the block
new_content = content[:insert_point] + kr_block + content[insert_point:]
open(r'C:\Users\Administrator\github\novelpick-website\best-cultivation-novels-2026.html', 'w', encoding='utf-8').write(new_content)
print('Done! Keep Reading block added.')
