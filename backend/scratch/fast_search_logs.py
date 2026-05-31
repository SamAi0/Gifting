import os
import re

WORKSPACE_DIR = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# Preset list of files/directories to scan (no recursive deep walk)
target_files = []

# 1. Direct root files
for f in os.listdir(WORKSPACE_DIR):
    f_path = os.path.join(WORKSPACE_DIR, f)
    if os.path.isfile(f_path) and f.endswith(('.txt', '.log', '.py')):
        target_files.append(f_path)

# 2. Files in workspace/scratch
scratch_dir = os.path.join(WORKSPACE_DIR, 'scratch')
if os.path.exists(scratch_dir):
    for f in os.listdir(scratch_dir):
        f_path = os.path.join(scratch_dir, f)
        if os.path.isfile(f_path) and f.endswith(('.txt', '.log', '.py')):
            target_files.append(f_path)

# 3. Files in backend/scratch
backend_scratch = os.path.join(WORKSPACE_DIR, 'backend', 'scratch')
if os.path.exists(backend_scratch):
    for f in os.listdir(backend_scratch):
        f_path = os.path.join(backend_scratch, f)
        if os.path.isfile(f_path) and f.endswith(('.txt', '.log', '.py')):
            # Skip checking scripts
            if f not in ['fast_search_logs.py', 'find_all_logs.py', 'check_my_ranges.py']:
                target_files.append(f_path)

ranges = [
    (270, 320, "270 - 320"),
    (500, 600, "500 - 600"),
    (830, 880, "830 - 880"),
    (1101, 1158, "1101 - 1158")
]

print("="*60)
print(f"Targeted search of {len(target_files)} key files in the workspace...")
print("="*60)

found_matches = {}

for file_path in target_files:
    rel_path = os.path.relpath(file_path, WORKSPACE_DIR)
    try:
        with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
            content = f.read()
            
        for start, end, label in ranges:
            matched_ids = []
            for pid in range(start, end + 1):
                # Search pattern
                if f"products/{pid}" in content or f"products\\{pid}" in content or f"product {pid}" in content:
                    matched_ids.append(pid)
                    
            if matched_ids:
                if rel_path not in found_matches:
                    found_matches[rel_path] = []
                found_matches[rel_path].append({
                    'range': label,
                    'matched_ids': matched_ids
                })
    except Exception as e:
        print(f"Error reading {rel_path}: {e}")

if found_matches:
    print(f"\nFound matches in {len(found_matches)} files:")
    for path, matches in found_matches.items():
        print(f"\nFile: '{path}'")
        for match in matches:
            print(f"  Range: {match['range']} -> Matched Product IDs: {match['matched_ids']}")
else:
    print("\nNo references to coordinates for these product ranges found in any local workspace logs or scripts.")
