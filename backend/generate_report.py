import os, json
with open('missing.json', 'r', encoding='utf-8') as f:
    missing = json.load(f)

lines = [
    "# Missing Images Report",
    f"Total Missing: {len(missing)}",
    "",
    "| Product Name | Expected File |",
    "|---|---|"
]

for item in missing:
    lines.append(f"| {item['name']} | `{item['file']}` |")

with open('../missing_images_report.md', 'w', encoding='utf-8') as f:
    f.write('\n'.join(lines))
