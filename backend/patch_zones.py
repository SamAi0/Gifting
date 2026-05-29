import os
import json

def main():
    backend_dir = os.path.dirname(os.path.abspath(__file__))
    json_path = os.path.join(backend_dir, '..', 'frontend', 'src', 'data', 'customization.json')

    if not os.path.exists(json_path):
        print(f"Error: customization.json not found at {json_path}")
        return

    with open(json_path, 'r') as f:
        data = json.load(f)

    # We only want to update the products that currently have only 2 zones 
    # (these are the ones we just added)
    updated_count = 0
    for item in data:
        if len(item.get('zones', [])) == 2:
            # Add 2 more text zones
            item['zones'].append({
                "id": "extra-1",
                "type": "text",
                "x": 500,
                "y": 350,
                "originX": "center",
                "originY": "center",
                "angle": 0,
                "maxWidth": 400,
                "maxChars": 20,
                "fontFamily": "Inter, sans-serif",
                "fontSize": 24,
                "minFontSize": 12,
                "fill": "#333333",
                "opacity": 1.0,
                "placeholder": "Extra Text 1"
            })
            item['zones'].append({
                "id": "extra-2",
                "type": "text",
                "x": 500,
                "y": 450,
                "originX": "center",
                "originY": "center",
                "angle": 0,
                "maxWidth": 400,
                "maxChars": 20,
                "fontFamily": "Inter, sans-serif",
                "fontSize": 20,
                "minFontSize": 12,
                "fill": "#666666",
                "opacity": 1.0,
                "placeholder": "Extra Text 2"
            })
            updated_count += 1

    with open(json_path, 'w') as f:
        json.dump(data, f, indent=2)

    print(f"Successfully updated {updated_count} products with 2 additional zones (Total 4 zones now).")
    print("Next step: Run 'python sync_customization.py' to update the database.")

if __name__ == "__main__":
    main()
