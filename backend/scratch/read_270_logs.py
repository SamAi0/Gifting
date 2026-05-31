import os

WORKSPACE_DIR = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
log_path = os.path.join(WORKSPACE_DIR, 'logs_261_270.txt')

print("="*60)
print(f"Reading logs for product 270 from {log_path}")
print("="*60)

with open(log_path, 'r', encoding='utf-8') as f:
    content = f.read()

lines = content.split('\n')
for i, line in enumerate(lines):
    if 'products/270' in line:
        print(f"Found products/270 at line {i+1}:")
        # print the next 20 lines
        for j in range(0, 25):
            if i + j < len(lines):
                print(f"  {i+j+1}: {lines[i+j]}")
        break
