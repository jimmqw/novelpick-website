import os, datetime
base = r'C:\Users\Administrator\.openclaw\agents\main\sessions'
files = [f for f in os.listdir(base) if f.endswith('.jsonl')]
apr24 = []
for f in sorted(files):
    path = os.path.join(base, f)
    mtime = os.path.getmtime(path)
    dt = datetime.datetime.fromtimestamp(mtime)
    size = os.path.getsize(path)
    if dt.date() == datetime.date(2026, 4, 24):
        apr24.append((dt, f, size))
        print(f'{dt.strftime("%Y-%m-%d %H:%M:%S")} | {f[:70]} | {size//1024}KB')
print()
print(f'Total April 24 files: {len(apr24)}')
