import os
import re

WORKSPACE_DIR = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
log_path = os.path.join(WORKSPACE_DIR, 'logs_261_270.txt')

print("="*60)
print(f"Analyzing all product IDs in {log_path}")
print("="*60)

with open(log_path, 'r', encoding='utf-8') as f:
    content = f.read()

# Find all occurrences of "products/ID"
matches = re.findall(r'products/(\d+)', content)
matched_ids = sorted(list(set(int(m) for m in matches)))

print(f"Found {len(matches)} total product references in the file.")
print(f"Distinct Product IDs: {matched_ids}")
