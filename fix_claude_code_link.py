fpath = r'C:\Users\Administrator\.openclaw\workspace\morai-website\best-ai-coding-assistants-2026.html'
with open(fpath, 'r', encoding='utf-8') as f:
    content = f.read()

old = '''<p>Senior developers working on significant refactoring or new service design will get the most from Claude Code. Its ability to reason about a codebase, propose plans, and execute autonomously is genuinely impressive. But it's not an autocomplete tool — you need to invest in learning how to prompt it effectively.</p>'''

new = '''<p>Senior developers working on significant refactoring or new service design will get the most from Claude Code. Its ability to reason about a codebase, propose plans, and execute autonomously is genuinely impressive. But it's not an autocomplete tool — you need to invest in learning how to prompt it effectively. <strong>See our full head-to-head:</strong> <a href="/claude-code-vs-cursor-vs-github-copilot-2026.html">Claude Code vs Cursor vs Copilot 2026</a></p>'''

if old in content:
    content = content.replace(old, new, 1)
    with open(fpath, 'w', encoding='utf-8') as f:
        f.write(content)
    print('SUCCESS')
else:
    # Try to find the line
    idx = content.find('Senior developers working on significant')
    if idx >= 0:
        print('Found at index', idx)
        print(repr(content[idx-20:idx+250]))
    else:
        print('NOT FOUND')