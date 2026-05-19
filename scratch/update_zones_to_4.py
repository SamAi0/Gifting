import os
import json

backend_dir = r"c:\Users\Asus\Downloads\New folder\Gifting\backend"
json_path = os.path.join(backend_dir, '..', 'frontend', 'src', 'data', 'customization.json')

with open(json_path, 'r', encoding='utf-8') as f:
    data = json.load(f)

updated_count = 0
for item in data:
    if item.get('productId', 0) >= 790:
        # Re-define the zones list to contain exactly 4 custom zones
        item['zones'] = [
            {
                "id": "name-1",
                "type": "text",
                "x": 500,
                "y": 150,
                "originX": "center",
                "originY": "center",
                "angle": 0,
                "maxWidth": 400,
                "maxChars": 15,
                "fontFamily": "Inter, sans-serif",
                "fontSize": 32,
                "minFontSize": 20,
                "fill": "#000000",
                "opacity": 1.0,
                "placeholder": "Your Name"
            },
            {
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
                "placeholder": "Extra Text"
            },
            {
                "id": "logo-2",
                "type": "image",
                "x": 500,
                "y": 450,
                "originX": "center",
                "originY": "center",
                "angle": 0,
                "width": 120,
                "height": 120,
                "placeholderImage": "/static/placeholders/logo.png"
            },
            {
                "id": "logo-1",
                "type": "image",
                "x": 500,
                "y": 250,
                "originX": "center",
                "originY": "center",
                "angle": 0,
                "width": 120,
                "height": 120,
                "placeholderImage": "/static/placeholders/logo.png"
            }
        ]
        updated_count += 1

with open(json_path, 'w', encoding='utf-8') as f:
    json.dump(data, f, indent=2)

print(f"Successfully updated zones for {updated_count} newly added products in customization.json.")
