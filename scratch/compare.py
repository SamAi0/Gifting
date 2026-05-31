import json
import subprocess
import os

def main():
    try:
        head_data = subprocess.check_output(['git', 'show', 'HEAD:frontend/src/data/customization.json'])
        head_json = json.loads(head_data.decode('utf-8'))
    except Exception as e:
        print("Error reading HEAD version:", e)
        return

    json_path = os.path.join('frontend', 'src', 'data', 'customization.json')
    if not os.path.exists(json_path):
        print("Current customization.json not found!")
        return

    with open(json_path, 'r', encoding='utf-8') as f:
        curr_json = json.load(f)

    head_slugs = {x.get('slug'): x for x in head_json if x.get('slug')}
    curr_slugs = {x.get('slug'): x for x in curr_json if x.get('slug')}

    added_slugs = set(curr_slugs.keys()) - set(head_slugs.keys())
    removed_slugs = set(head_slugs.keys()) - set(curr_slugs.keys())

    print("=" * 60)
    print("ADDED SLUGS:", len(added_slugs))
    for s in sorted(list(added_slugs))[:10]:
        print(f"  + {s}")
    if len(added_slugs) > 10:
        print(f"  ... and {len(added_slugs)-10} more")

    print("\nREMOVED SLUGS:", len(removed_slugs))
    for s in sorted(list(removed_slugs))[:10]:
        print(f"  - {s}")
    if len(removed_slugs) > 10:
        print(f"  ... and {len(removed_slugs)-10} more")

    # Check for name/slug changes on the same productId
    head_ids = {x.get('productId'): x for x in head_json if x.get('productId')}
    curr_ids = {x.get('productId'): x for x in curr_json if x.get('productId')}

    renamed = []
    for pid, curr_item in curr_ids.items():
        if pid in head_ids:
            head_item = head_ids[pid]
            if head_item.get('productName') != curr_item.get('productName') or head_item.get('slug') != curr_item.get('slug'):
                renamed.append((pid, head_item, curr_item))

    print(f"\nRENAMED PRODUCTS BY ID: {len(renamed)}")
    for pid, old, new in renamed:
        print(f"  ID {pid}:")
        print(f"    OLD: Name='{old.get('productName')}', Slug='{old.get('slug')}'")
        print(f"    NEW: Name='{new.get('productName')}', Slug='{new.get('slug')}'")

if __name__ == '__main__':
    main()
