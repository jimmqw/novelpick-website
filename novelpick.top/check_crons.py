import subprocess, json
result = subprocess.run(['openclaw', 'cron', 'list', '--json'], capture_output=True, text=True)
lines = result.stdout.split('\n')
# Find JSON block
start = -1
for i, line in enumerate(lines):
    if line.strip().startswith('['):
        start = i
        break
if start >= 0:
    json_str = '\n'.join(lines[start:])
    try:
        data = json.loads(json_str)
        for cron in data:
            name = cron.get('name', '')
            status = cron.get('lastStatus', '')
            err = cron.get('lastError', '')
            cons = cron.get('consecutiveErrors', 0)
            if status == 'error' or cons > 0:
                print(f'ERROR: {name}')
                print(f'  cons={cons}, status={status}')
                print(f'  err: {err[:100]}')
                print()
    except Exception as e:
        print(f'JSON parse error: {e}')
else:
    print('No JSON found')
    print(result.stdout[:500])