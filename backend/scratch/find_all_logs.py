import os
import re

WORKSPACE_DIR = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

ranges = [
    (270, 320, "270 - 320"),
    (500, 600, "500 - 600"),
    (830, 880, "830 - 880"),
    (1101, 1158, "1101 - 1158")
]

print("="*60)
print(f"Deep searching the entire project workspace for coordinate logs...")
print("="*60)

found_files = {}

for root, dirs, files in os.walk(WORKSPACE_DIR):
    if any(ignore in root for ignore in ['venv', 'node_modules', '.git', '__pycache__']):
        continue
        
    for file in files:
        file_path = os.path.join(root, file)
        # Skip this script and generated files
        if file in ['find_all_logs.py', 'check_my_ranges.py', 'ranges_status_report.txt']:
            continue
            
        try:
            with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
                content = f.read()
                
            # Quick check if it contains coordinate patterns
            if '"x":' in content or '"y":' in content or 'Zone Update' in content or 'CanvasCustomizer' in content:
                # Search for any product ID in our ranges
                for start, end, label in ranges:
                    matched_ids = []
                    for pid in range(start, end + 1):
                        # Matches "products/ID" or "products\\ID" or "ID" surrounded by non-digits
                        pattern = rf'\b{pid}\b'
                        if re.search(pattern, content):
                            matched_ids.append(pid)
                            
                    if matched_ids:
                        rel_path = os.path.relpath(file_path, WORKSPACE_DIR)
                        if rel_path not in found_files:
                            found_files[rel_path] = []
                        found_files[rel_path].append({
                            'range': label,
                            'matched_ids': matched_ids
                        })
        except Exception:
            pass

if found_files:
    print(f"Found {len(found_files)} files containing references to product IDs in our ranges:")
    for path, matches in found_files.items():
        print(f"\nFile: '{path}'")
        for match in matches:
            print(f"  Range: {match['range']} -> Matched IDs: {match['matched_ids']}")
else:
    print("\nNo log files or scripts found containing coordinates for these ranges anywhere in the project!")
