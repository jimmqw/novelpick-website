# -*- coding: utf-8 -*-
import os, re

files = {
    'morai': [
        r'C:\Users\Administrator\.openclaw\workspace\morai.top\best-ai-agents-2026.html',
        r'C:\Users\Administrator\.openclaw\workspace\morai.top\best-ai-writing-tools-2026.html',
        r'C:\Users\Administrator\.openclaw\workspace\morai.top\best-ai-video-generation-tools-2026.html',
        r'C:\Users\Administrator\.openclaw\workspace\morai.top\best-ai-note-taking-tools-2026.html',
        r'C:\Users\Administrator\.openclaw\workspace\morai.top\github-copilot-review-2026.html',
    ],
    'novelpick': [
        r'C:\Users\Administrator\.openclaw\workspace\novelpick.top\best-reincarnation-web-novels-2026.html',
        r'C:\Users\Administrator\.openclaw\workspace\novelpick.top\top-romance-web-novels-2026.html',
        r'C:\Users\Administrator\.openclaw\workspace\novelpick.top\best-time-travel-web-novels-2026.html',
        r'C:\Users\Administrator\.openclaw\workspace\novelpick.top\books-like-solo-leveling.html',
        r'C:\Users\Administrator\.openclaw\workspace\novelpick.top\best-cultivation-novels-2026.html',
    ],
}

for site, paths in files.items():
    for path in paths:
        try:
            with open(path, 'r', encoding='utf-8') as f:
                content = f.read()
            name = os.path.basename(path)

            has_baidu = 'hm.baidu.com' in content
            has_og_site = 'og:site_name' in content
            has_share = 'share-section' in content or 'share-buttons' in content
            has_copyright = 'copyright' in content.lower() or '&copy;' in content

            # Check for AI content warning phrases
            ai_phrases = ['we carefully evaluated', 'our tests show', 'in our experience', 'extensive testing', 'comprehensive analysis']
            ai_warnings = [p for p in ai_phrases if p.lower() in content.lower()]

            # Check for empty/vague sections
            has_empty = 'no clear conclusion' in content.lower() or 'in conclusion' not in content.lower()

            # Check BLUF: h2 sections with conclusions first
            h2_sections = re.findall(r'<h2[^>]*>(.*?)</h2>', content, re.IGNORECASE)

            # Check prev-next links
            has_prev_next = 'prev-next' in content

            issue_list = []
            if not has_baidu:
                issue_list.append('NO_BAIDU')
            if not has_og_site:
                issue_list.append('NO_OG_SITE')
            if not has_share:
                issue_list.append('NO_SHARE')
            if not has_copyright:
                issue_list.append('NO_COPYRIGHT')
            if ai_warnings:
                issue_list.append('VAGUE_AI_REF:' + str(len(ai_warnings)))
            if not has_prev_next:
                issue_list.append('NO_PREV_NEXT')

            status = 'ISSUE' if issue_list else 'OK'
            print(f'[{status}] {site}/{name}: {issue_list}')

        except Exception as e:
            print(f'[ERR] {path}: {e}')