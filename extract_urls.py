import re, glob, os

urls = set()
files = glob.glob('e:/epwinds/*.html') + glob.glob('e:/epwinds/*/*.html')
for f in files:
    with open(f, 'r', encoding='utf-8', errors='ignore') as fh:
        text = fh.read()
    for m in re.finditer(r'https://files\.peachworlds\.com/[^"\'\s<>]+', text):
        urls.add(m.group(0))

print(f'Found {len(urls)} unique URLs:')
for u in sorted(urls):
    print(u)
