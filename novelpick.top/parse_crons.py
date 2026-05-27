import re
with open(r'C:\Users\Administrator\.openclaw\workspace\cron_list.json', 'rb') as f:
    raw = f.read()
text = raw.decode('utf-8', errors='replace')
pattern = r'"name":\s*"([^"]+)".*?"lastStatus":\s*"([^"]+)".*?"lastError":\s*"([^"]*)".*?"consecutiveErrors":\s*(\d+)'
matches = re.findall(pattern, text, re.DOTALL)
for name, status, err, cons in matches:
    if status == 'error' or int(cons) > 0:
        print('ERROR: ' + name + ' (cons=' + cons + ')')
        err_short = err[:100] if err else ''
        print('  err: ' + err_short)
        print()