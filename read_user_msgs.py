import json, os

base = r'C:\Users\Administrator\.openclaw\agents\main\sessions'
files_to_check = [
    'd44451ce-6828-4ab4-bcaa-8b787115fab0.jsonl',
    'ae37a6af-cb78-49cd-a93f-e5681af9823e.jsonl',
    '59cabae5-97aa-486c-ac15-5863cf41562d.jsonl',
    '3023e75c-c34d-4592-ae4b-c24c29b5b951.jsonl',
    'a6d8eb39-9438-4362-bc7f-eab5866df665.jsonl',
    'a9ac26e7-c6fd-4e4d-a276-2a90cd2d1d67.jsonl',
]

for fname in files_to_check:
    fpath = os.path.join(base, fname)
    if not os.path.exists(fpath):
        print(f'NOT FOUND: {fname}')
        continue
    size = os.path.getsize(fpath)
    print(f'\n=== {fname} ({size//1024}KB) ===')
    count = 0
    try:
        with open(fpath, 'r', encoding='utf-8', errors='replace') as f:
            for line in f:
                try:
                    obj = json.loads(line.strip())
                    if obj.get('type') != 'message':
                        continue
                    msg = obj.get('message', {})
                    if msg.get('role') != 'user':
                        continue
                    for c in msg.get('content', []):
                        if c.get('type') != 'text':
                            continue
                        text = c['text']
                        if len(text) < 10:
                            continue
                        ts = msg.get('timestamp', '')
                        count += 1
                        display = text[:500].replace('\n', ' | ')
                        print(f'  [{ts}] {display}')
                        print()
                except Exception as e:
                    pass
        print(f'  Total: {count}')
    except Exception as e:
        print(f'  Error: {e}')
