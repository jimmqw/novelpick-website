fpath = r'C:\Users\Administrator\.openclaw\workspace\morai-website\best-ai-coding-assistants-2026.html'
with open(fpath, 'r', encoding='utf-8') as f:
    content = f.read()

old = 'Senior developers working on significant refactoring or new service design will get the most from Claude Code. Its ability to reason about a codebase, propose plans, and execute autonomously is genuinely impressive. But it\'s not an autocomplete tool \u2014 you need to invest in learning how to prompt it effectively.'

new = old + ' <strong>See our full head-to-head:</strong> <a href="/claude-code-vs-cursor-vs-github-copilot-2026.html">Claude Code vs Cursor vs Copilot 2026</a>'

if old in content:
    content = content.replace(old, new, 1)
    with open(fpath, 'w', encoding='utf-8') as f:
        f.write(content)
    print('SUCCESS')
else:
    # Check what encoding issues might exist
    idx = content.find('Senior developers working on significant refactoring or new service design will get the most from Claude Code')
    if idx >= 0:
        print('Found partial at index', idx)
        segment = content[idx:idx+300]
        print(repr(segment))
        # Try replacing the segment between the quotes
        content2 = content.replace(
            'Senior developers working on significant refactoring or new service design will get the most from Claude Code. Its ability to reason about a codebase, propose plans, and execute autonomously is genuinely impressive. But it\'s not an autocomplete tool \u2014 you need to invest in learning how to prompt it effectively.',
            'Senior developers working on significant refactoring or new service design will get the most from Claude Code. Its ability to reason about a codebase, propose plans, and execute autonomously is genuinely impressive. But it\'s not an autocomplete tool \u2014 you need to invest in learning how to prompt it effectively. <strong>See our full head-to-head:</strong> <a href="/claude-code-vs-cursor-vs-github-copilot-2026.html">Claude Code vs Cursor vs Copilot 2026</a>'
        )
        with open(fpath, 'w', encoding='utf-8') as f:
            f.write(content2)
        print('SUCCESS (fallback)')
    else:
        print('NOT FOUND')