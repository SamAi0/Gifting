import os
import sys
import re

# Set stdout to use utf-8 if possible or ignore errors
sys.stdout.reconfigure(encoding='utf-8')

WORKSPACE_DIR = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
last_message_path = os.path.join(WORKSPACE_DIR, 'last_message.txt')

print("="*60)
print(f"Analyzing all log files in: {WORKSPACE_DIR}")
print("="*60)

log_files = [
    'last_message.txt',
    'full_logs.txt',
    'full_logs2.txt',
    'full_logs3.txt',
    'logs_101_150.txt',
    'logs_151_200.txt',
    'logs_201_260.txt',
    'logs_261_270.txt',
    'logs_264_3.txt'
]

ranges = [
    (270, 320, "270 - 320"),
    (500, 600, "500 - 600"),
    (830, 880, "830 - 880"),
    (1101, 1158, "1101 - 1158")
]

for filename in log_files:
    file_path = os.path.join(WORKSPACE_DIR, filename)
    if not os.path.exists(file_path):
        continue
        
    print(f"\nChecking file: {filename}")
    
    encodings = ['utf-16le', 'utf-16', 'utf-8', 'latin-1']
    content = None
    for enc in encodings:
        try:
            with open(file_path, 'r', encoding=enc) as f:
                content = f.read()
            break
        except Exception:
            pass
            
    if content is None:
        print("  Could not read file!")
        continue
        
    # Search for product ID matches in the content
    lines = content.split('\n')
    found_any = False
    
    for start, end, label in ranges:
        matched_ids = []
        for pid in range(start, end + 1):
            # regex to find product ID in path or line
            pattern = rf'(?:products/|products\\|product\s+)\b{pid}\b'
            if re.search(pattern, content, re.IGNORECASE) or rf'products/{pid}' in content:
                matched_ids.append(pid)
                
        if matched_ids:
            found_any = True
            print(f"  Range {label}: Matches found for IDs {matched_ids[:10]}... (Total: {len(matched_ids)} products)")
            # Print a few matching lines
            print("  Sample lines:")
            count = 0
            for i, line in enumerate(lines):
                for pid in matched_ids:
                    if rf'products/{pid}' in line or rf'products\\{pid}' in line or rf'product {pid}' in line or re.search(rf'\b{pid}\b', line):
                        # print context of lines around it
                        print(f"    Line {i+1}: {line.strip()[:100]}")
                        # print next 3 lines for context (e.g. x, y, angle)
                        for j in range(1, 4):
                            if i + j < len(lines):
                                print(f"      +{j}: {lines[i+j].strip()[:100]}")
                        count += 1
                        break
                if count >= 3:
                    break
    if not found_any:
        print("  No product matches in the targeted ranges found.")
