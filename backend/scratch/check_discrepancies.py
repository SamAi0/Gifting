import os
import json
import sqlite3

def main():
    # 1. Load customization.json (frontend)
    frontend_json_path = r"c:\Users\Asus\OneDrive\Pictures\Camera Roll 1\Gifting\frontend\src\data\customization.json"
    try:
        with open(frontend_json_path, 'r', encoding='utf-8') as f:
            custom_data = json.load(f)
    except Exception as e:
        print(f"Error reading frontend JSON: {e}")
        return

    # Map product ID -> frontend image name
    frontend_images = {}
    for item in custom_data:
        pid = item.get('productId')
        if pid:
            frontend_images[pid] = os.path.basename(item.get('baseImage', ''))
    
    # 2. Load backend database
    db_path = r"c:\Users\Asus\OneDrive\Pictures\Camera Roll 1\Gifting\backend\db.sqlite3"
    backend_images = {}
    try:
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()
        cursor.execute("SELECT id, image FROM products_product")
        for row in cursor.fetchall():
            pid, img_path = row
            backend_images[pid] = os.path.basename(img_path) if img_path else ""
    except Exception as e:
        print(f"Error reading database: {e}")
        return
    finally:
        conn.close()

    # 3. Check actual files
    actual_files_dir = r"c:\Users\Asus\OneDrive\Pictures\Camera Roll 1\Gifting\frontend\public\static\products"
    try:
        actual_files = set(os.listdir(actual_files_dir))
    except Exception as e:
        print(f"Error reading files directory: {e}")
        return

    # 4. Compare
    mismatches = []
    missing_in_files = []

    all_pids = set(frontend_images.keys()).union(set(backend_images.keys()))

    for pid in all_pids:
        f_img = frontend_images.get(pid, "").lower()
        b_img = backend_images.get(pid, "").lower()

        # Check mismatch between frontend json and backend db
        if f_img and b_img and f_img != b_img:
            mismatches.append({"pid": pid, "frontend": f_img, "backend": b_img})

        # Check if backend image is missing in actual files
        if b_img:
            # Note: actual_files is case sensitive in Python by default, but Windows is not.
            # We will lower-case actual files for comparison
            lower_actual = {f.lower() for f in actual_files}
            if b_img not in lower_actual:
                # wait, maybe it's missing entirely
                missing_in_files.append({"pid": pid, "backend_expects": b_img, "frontend_expects": f_img})

    print(f"Total products in Frontend JSON: {len(frontend_images)}")
    print(f"Total products in Backend DB: {len(backend_images)}")
    print(f"Total actual image files: {len(actual_files)}")
    
    print("\n--- Mismatches between Frontend JSON and Backend DB (Showing first 20) ---")
    for m in mismatches[:20]:
        print(f"ID {m['pid']}: Frontend expects '{m['frontend']}', Backend provides '{m['backend']}'")
    print(f"Total mismatches: {len(mismatches)}")

    print("\n--- Images missing from disk (Backend expects them but they are not in folder) (Showing first 20) ---")
    for m in missing_in_files[:20]:
        print(f"ID {m['pid']}: Backend expects '{m['backend_expects']}', Frontend JSON expects '{m['frontend_expects']}'")
    print(f"Total missing from disk: {len(missing_in_files)}")

if __name__ == '__main__':
    main()
