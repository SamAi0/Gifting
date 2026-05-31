import os
import sys
import json
import re
import django

# Setup Django settings
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'core.settings')
try:
    django.setup()
    from products.models import Product
    DJANGO_AVAILABLE = True
except Exception as e:
    DJANGO_AVAILABLE = False
    print(f"[WARNING] Django setup failed or not available: {e}")

WORKSPACE_DIR = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
FRONTEND_JSON_PATH = os.path.join(WORKSPACE_DIR, 'frontend', 'src', 'data', 'customization.json')

RANGES = [
    (270, 320, "270 - 320"),
    (500, 600, "500 - 600"),
    (830, 880, "830 - 880"),
    (1101, 1158, "1101 - 1158")
]

def check_in_db():
    if not DJANGO_AVAILABLE:
        return {}
    
    results = {}
    print("\n" + "="*50)
    print("CHECKING DJANGO DATABASE")
    print("="*50)
    
    for start, end, label in RANGES:
        in_db = 0
        with_config = 0
        details = []
        
        # We query by ID
        products = Product.objects.filter(id__gte=start, id__lte=end).order_by('id')
        in_db = products.count()
        
        for p in products:
            has_conf = False
            config_data = []
            if p.customization_config:
                try:
                    zones = json.loads(p.customization_config)
                    if isinstance(zones, list) and len(zones) > 0:
                        has_conf = True
                        with_config += 1
                        for z in zones:
                            config_data.append({
                                'id': z.get('id'),
                                'name': z.get('name'),
                                'x': z.get('x'),
                                'y': z.get('y'),
                                'angle': z.get('angle')
                            })
                except Exception:
                    pass
            details.append({
                'id': p.id,
                'name': p.name,
                'slug': p.slug,
                'has_config': has_conf,
                'zones': config_data
            })
            
        results[label] = {
            'count': in_db,
            'with_config': with_config,
            'details': details
        }
        print(f"Range {label}: Found {in_db} products in DB. {with_config} have customization zones configured.")
        
    return results

def check_in_json():
    results = {}
    print("\n" + "="*50)
    print("CHECKING frontend/src/data/customization.json")
    print("="*50)
    
    if not os.path.exists(FRONTEND_JSON_PATH):
        print(f"[ERROR] customization.json not found at {FRONTEND_JSON_PATH}")
        return results
        
    with open(FRONTEND_JSON_PATH, 'r', encoding='utf-8') as f:
        try:
            data = json.load(f)
        except Exception as e:
            print(f"[ERROR] Failed to parse customization.json: {e}")
            return results
            
    # Build maps of customization.json by ID and by Slug
    by_id = {}
    for item in data:
        pid = item.get('productId')
        if pid is not None:
            try:
                by_id[int(pid)] = item
            except ValueError:
                pass
                
    for start, end, label in RANGES:
        found_in_json = 0
        details = []
        
        for pid in range(start, end + 1):
            if pid in by_id:
                found_in_json += 1
                item = by_id[pid]
                zones = item.get('zones', [])
                zone_details = []
                for z in zones:
                    zone_details.append({
                        'id': z.get('id'),
                        'name': z.get('name'),
                        'x': z.get('x'),
                        'y': z.get('y'),
                        'angle': z.get('angle')
                    })
                details.append({
                    'id': pid,
                    'name': item.get('productName'),
                    'slug': item.get('slug'),
                    'zones': zone_details
                })
                
        results[label] = {
            'count': found_in_json,
            'details': details
        }
        print(f"Range {label}: Found {found_in_json} products in customization.json.")
        
    return results

def search_in_logs():
    print("\n" + "="*50)
    print("SEARCHING RAW LOG FILES AND SCRIPTS")
    print("="*50)
    
    # We will search the following extensions
    target_extensions = ('.txt', '.py', '.log')
    found_occurrences = {}
    
    for start, end, label in RANGES:
        found_occurrences[label] = []
        
    # Walk directory to find files
    for root, dirs, files in os.walk(WORKSPACE_DIR):
        # Skip node_modules and venv
        if 'node_modules' in root or 'venv' in root or '.git' in root:
            continue
            
        for file in files:
            if file.endswith(target_extensions):
                file_path = os.path.join(root, file)
                # Skip the checker script itself
                if file == 'check_my_ranges.py':
                    continue
                    
                try:
                    with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
                        content = f.read()
                        
                    for start, end, label in RANGES:
                        # Search patterns like "products/ID" or "ID:" or zone updates with ID
                        matches = []
                        for pid in range(start, end + 1):
                            # Look for products/pid
                            pattern = rf'products/{pid}\b'
                            if re.search(pattern, content):
                                matches.append(pid)
                                
                        if matches:
                            rel_path = os.path.relpath(file_path, WORKSPACE_DIR)
                            found_occurrences[label].append({
                                'file': rel_path,
                                'matched_ids': sorted(list(set(matches)))
                            })
                except Exception as e:
                    pass
                    
    for label, occurrences in found_occurrences.items():
        print(f"Range {label} log references:")
        if not occurrences:
            print("  No references found in workspace files/logs.")
        for occ in occurrences:
            print(f"  In '{occ['file']}': matches product IDs: {occ['matched_ids']}")
            
    return found_occurrences

if __name__ == '__main__':
    # Fix the typo from earlier
    DJANGO_AVAILABLE = 'DJANGO_AVAILABLE' in globals() and DJANGO_AVAILABLE
    
    db_res = check_in_db()
    json_res = check_in_json()
    log_res = search_in_logs()
    
    # Write summary report to a text file in scratch
    report_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'ranges_status_report.txt')
    with open(report_path, 'w', encoding='utf-8') as rf:
        rf.write("============================================================\n")
        rf.write("PRODUCT RANGES CUSTOMIZATION COORDINATES STATUS REPORT\n")
        rf.write("============================================================\n\n")
        
        for start, end, label in RANGES:
            rf.write(f"RANGE: {label} (Target {end - start + 1} products)\n")
            rf.write("-" * 60 + "\n")
            
            # DB Info
            db_info = db_res.get(label, {'count': 0, 'with_config': 0, 'details': []})
            rf.write(f"1. Django Database Status:\n")
            rf.write(f"   - Total products found in DB range: {db_info['count']}\n")
            rf.write(f"   - Products with zones in DB: {db_info['with_config']}\n")
            
            # Json Info
            json_info = json_res.get(label, {'count': 0, 'details': []})
            rf.write(f"2. customization.json Status:\n")
            rf.write(f"   - Total products found in JSON: {json_info['count']}\n\n")
            
            # Log occurrences
            rf.write(f"3. References in raw workspace logs/files:\n")
            logs_found = log_res.get(label, [])
            if not logs_found:
                rf.write("   - None\n")
            else:
                for lf in logs_found:
                    rf.write(f"   - File: {lf['file']}\n")
                    rf.write(f"     Matched Product IDs: {lf['matched_ids']}\n")
            
            rf.write("\nDetailed list of configured products in this range:\n")
            # We combine the details
            configured_pids = set()
            details_map = {}
            
            for p in db_info['details']:
                if p['has_config']:
                    configured_pids.add(p['id'])
                    details_map[p['id']] = {
                        'name': p['name'],
                        'slug': p['slug'],
                        'db_zones': p['zones'],
                        'json_zones': []
                    }
                    
            for p in json_info['details']:
                pid = p['id']
                configured_pids.add(pid)
                if pid not in details_map:
                    details_map[pid] = {
                        'name': p['name'],
                        'slug': p['slug'],
                        'db_zones': [],
                        'json_zones': p['zones']
                    }
                else:
                    details_map[pid]['json_zones'] = p['zones']
                    
            if not configured_pids:
                rf.write("   NO PRODUCTS ARE CONFIGURED WITH CUSTOMIZATION COORDINATES IN THIS RANGE.\n")
            else:
                for pid in sorted(configured_pids):
                    p_det = details_map[pid]
                    rf.write(f"   - ID: {pid} | Name: {p_det['name']} | Slug: {p_det['slug']}\n")
                    if p_det['db_zones']:
                        rf.write("     Database Zones:\n")
                        for z in p_det['db_zones']:
                            rf.write(f"       * {z['id']} ({z['name']}): x={z['x']}, y={z['y']}, angle={z['angle']}\n")
                    else:
                        rf.write("     Database Zones: NONE\n")
                        
                    if p_det['json_zones']:
                        rf.write("     JSON Zones:\n")
                        for z in p_det['json_zones']:
                            rf.write(f"       * {z['id']} ({z['name']}): x={z['x']}, y={z['y']}, angle={z['angle']}\n")
                    else:
                        rf.write("     JSON Zones: NONE\n")
            rf.write("\n" + "="*60 + "\n\n")
            
    print(f"\n[SUCCESS] Wrote full detailed report to: {report_path}")
