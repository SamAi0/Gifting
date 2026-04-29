# Customization Zones - How It Works

## Understanding the Data Flow

```
customization.json (Reference File)
        ↓
    [MANUAL SYNC NEEDED]
        ↓
Database (Product.customization_config field)
        ↓
    [API: /api/products/]
        ↓
Frontend (CanvasCustomizer component)
        ↓
    [Displayed on localhost]
```

## Why Changes to customization.json Don't Show Immediately

The `customization.json` file is a **reference/template file** that you can edit, but it's **NOT automatically synced** to your application. Here's why:

1. **Backend stores data in database** - The Product model has a `customization_config` field (TextField) that stores JSON
2. **Frontend fetches from API** - When you view a product, it calls `/api/products/{id}` which reads from the database
3. **JSON file is for convenience** - It's easier to edit zones in a JSON file than in Django admin

## How to Update Customization Zones

### Method 1: Sync Script (Recommended) ✨

After making changes to `customization.json`:

```bash
cd backend
python sync_customization.py
```

This will:
- Read your `customization.json` file
- Update all products in the database
- Show you which products were updated

### Method 2: Django Admin

1. Go to `http://127.0.0.1:8000/admin/`
2. Login with your superuser credentials
3. Click on **Products** → Select a product
4. Edit the **Customization config** field (JSON format)
5. Click **Save**

Example JSON for customization_config:
```json
[
  {
    "id": "text-zone-1",
    "type": "text",
    "x": 500,
    "y": 500,
    "originX": "center",
    "originY": "center",
    "angle": 45,
    "maxWidth": 400,
    "maxChars": 10,
    "fontFamily": "Inter, sans-serif",
    "fontSize": 48,
    "minFontSize": 20,
    "fill": "#000000",
    "opacity": 1.0,
    "placeholder": "Your Name"
  }
]
```

### Method 3: Django Shell

```bash
cd backend
python manage.py shell
```

```python
from products.models import Product
import json

product = Product.objects.get(id=1)
config = json.loads(product.customization_config)

# Update angle
config[0]['angle'] = 45

# Save back
product.customization_config = json.dumps(config)
product.save()
```

## Available Zone Properties

| Property | Type | Description | Example |
|----------|------|-------------|---------|
| `id` | string | Unique identifier | `"text-zone-1"` |
| `type` | string | Zone type | `"text"` |
| `x` | number | X position (0-1000 scale) | `500` |
| `y` | number | Y position (0-1000 scale) | `500` |
| `originX` | string | Horizontal origin | `"center"`, `"left"`, `"right"` |
| `originY` | string | Vertical origin | `"center"`, `"top"`, `"bottom"` |
| `angle` | number | Rotation in degrees | `0`, `45`, `90` |
| `maxWidth` | number | Maximum width (0-1000 scale) | `400` |
| `maxChars` | number | Maximum characters allowed | `20` |
| `fontFamily` | string | Font family | `"Inter, sans-serif"` |
| `fontSize` | number | Initial font size | `48` |
| `minFontSize` | number | Minimum font size (auto-fit) | `20` |
| `fill` | string | Text color (hex) | `"#000000"` |
| `opacity` | number | Transparency (0-1) | `1.0` |
| `placeholder` | string | Default text | `"Your Name"` |
| `isCurved` | boolean | Enable curved text | `true`/`false` |
| `curveRadius` | number | Radius for curved text | `150` |
| `charSpacing` | number | Character spacing for curved | `8` |

## Common Issues

### ❌ "I changed the angle in customization.json but nothing changed"
**Solution:** Run the sync script:
```bash
cd backend
python sync_customization.py
```

### ❌ "Text is not appearing at the right position"
**Solution:** 
- Positions use a 0-1000 scale, which gets converted to 500x500 canvas
- `x: 500, y: 500` = center of the canvas
- Adjust x/y values and re-sync

### ❌ "Changes show in development but not in production"
**Solution:**
- Make sure to run the sync script before deploying
- Or update via Django admin in production

## Pro Tips 💡

1. **Use Dev Mode for Visual Editing**
   - Add `?dev=true` to your URL
   - Drag zones to reposition visually
   - Click "Copy Config JSON" button
   - Paste the copied JSON into customization.json
   - Run sync script

2. **Test Incrementally**
   - Change one property at a time
   - Sync and verify before making more changes

3. **Backup Before Bulk Changes**
   - Export current database before major updates
   - Keep version control of customization.json

## Quick Workflow

1. Edit `customization.json` with your changes (angle, position, etc.)
2. Run: `cd backend && python sync_customization.py`
3. Refresh your localhost page
4. Verify changes appear correctly
5. Repeat as needed

## Need Help?

If you're still having issues:
1. Check browser console for errors
2. Verify the product ID matches between JSON and database
3. Make sure Django server is running
4. Try hard refresh (Ctrl+Shift+R) in browser
