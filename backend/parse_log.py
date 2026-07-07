import re

with open('batch6_log.txt', 'r', encoding='utf-8') as f:
    lines = f.readlines()

out = []
for line in lines:
    m = re.search(r'g:\d+:(.*)', line)
    if m:
        out.append(m.group(1))
    elif line.startswith("**Warning"):
        out.append(line.strip())
    elif line.startswith("- "):
        out.append(line.strip())

with open(r'C:\Users\Asus\.gemini\antigravity-ide\brain\0b0b6385-9acb-47b0-88ab-49791b5084f4\batch6_prices.md', 'w', encoding='utf-8') as f:
    f.write('\n'.join(out))
