import re, os

# AI language replacements
replacements = {
    'unmatched': 'excellent',
    'Unmatched': 'Excellent',
    'cutting-edge': 'advanced',
    'Cutting-edge': 'Advanced',
    'unbeatable': 'excellent',
    'Unbeatable': 'Excellent',
    'game-changer': 'useful tool',
    'game-changing': 'useful',
    'groundbreaking': 'notable',
    'revolutionize': 'improve',
    'revolutionizing': 'improving',
}

# Only fix high-traffic pages
priority_files = [
    'best-ai-agents-2026.html',
    'best-ai-coding-assistants-2026.html',
    'best-ai-chatbots-2026.html',
    'best-ai-image-generators-2026-comparison.html',
    'best-ai-coding-tools-2026.html',
    'claude-3-7-sonnet-review.html',
    'cursor-ai-review.html',
    'chatgpt-vs-claude.html',
    'chatgpt-vs-claude-vs-gemini-2026.html',
    'ai-agent-tools-2026.html',
    'ai-code-review-tools.html',
    'ai-image-generators.html',
    'ai-writing-tools.html',
    'best-ai-design-tools-2026.html',
    'best-ai-meeting-tools-2026.html',
    'best-ai-note-taking-tools-2026.html',
    'best-ai-research-assistants-2026.html',
    'how-ai-agents-transform-knowledge-work-2026.html',
    'best-ai-agents-2026.html',
    'best-action-fantasy-web-novels-2026.html',
    'best-apocalypse-and-survival-novels.html',
    'best-apocalypse-survival-web-novels.html',
    'best-enemies-to-lovers-romance-novels.html',
    'best-historical-fantasy-novels.html',
    'best-progression-fantasy-novels.html',
    'best-reincarnation-novels.html',
    'best-urban-fantasy-novels-2026-v2.html',
    'best-cultivation-novels-2026.html',
    'best-solo-leveling-novels.html',
    'books-like-solo-leveling.html',
]

site_path = r'C:\Users\Administrator\github\morai-site'
fixed = 0
for fname in priority_files:
    fpath = os.path.join(site_path, fname)
    if not os.path.exists(fpath):
        continue
    content = open(fpath, encoding='utf-8', errors='ignore').read()
    original = content
    for phrase, replacement in replacements.items():
        # Case-insensitive replacement
        content = re.sub(r'\b' + re.escape(phrase) + r'\b', replacement, content, flags=re.IGNORECASE)
    
    if content != original:
        with open(fpath, 'w', encoding='utf-8') as f:
            f.write(content)
        print(f'Fixed: {fname}')
        fixed += 1

print(f'\nTotal fixed: {fixed} files (morai)')

# Now novelpick
site_path2 = r'C:\Users\Administrator\github\novelpick-site'
novelpick_priority = [
    'best-action-fantasy-web-novels-2026.html',
    'best-apocalypse-and-survival-novels.html',
    'best-apocalypse-survival-web-novels.html',
    'best-enemies-to-lovers-romance-novels.html',
    'best-historical-fantasy-novels.html',
    'best-progression-fantasy-novels.html',
    'best-reincarnation-novels.html',
    'best-cultivation-novels-2026.html',
    'best-solo-leveling-novels.html',
    'best-urban-fantasy-novels-2026-v2.html',
]

fixed2 = 0
for fname in novelpick_priority:
    fpath = os.path.join(site_path2, fname)
    if not os.path.exists(fpath):
        continue
    content = open(fpath, encoding='utf-8', errors='ignore').read()
    original = content
    for phrase, replacement in replacements.items():
        content = re.sub(r'\b' + re.escape(phrase) + r'\b', replacement, content, flags=re.IGNORECASE)
    
    if content != original:
        with open(fpath, 'w', encoding='utf-8') as f:
            f.write(content)
        print(f'Fixed: {fname}')
        fixed2 += 1

print(f'\nTotal fixed: {fixed2} files (novelpick)')
