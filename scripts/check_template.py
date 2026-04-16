import re
import os

template_path = r'C:\Users\Administrator\Desktop\贾维斯网站模板\morai-website'
if not os.path.exists(template_path):
    print("Template path not found")
    exit()

files = os.listdir(template_path)
print("Template files:", files[:10])

# check a sample article page
sample = r'C:\Users\Administrator\Desktop\GitHub\morai-website\best-ai-agents-2026.html'
if os.path.exists(sample):
    content = open(sample, encoding='utf-8').read()
    # find article-body
    idx = content.find('article-body')
    if idx >= 0:
        print(f"\narticle-body found at {idx}")
        print("Context:", content[idx-100:idx+500])
    else:
        print("\nNo article-body found")
        idx2 = content.find('article-layout')
        print("article-layout at", idx2)
        if idx2 >= 0:
            print(content[idx2:idx2+500])
else:
    print("Sample file not found")
