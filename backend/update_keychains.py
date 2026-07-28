import os
import sys
import json
import django

# Setup Django settings
sys.path.append(os.path.dirname(os.path.abspath(__file__)))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'core.settings')
django.setup()

from products.models import Product
from sync_customization import sync_customization_zones

# Targets coordinate updates definition (Batches 1 & 2)
TARGETS = {
    # Batch 1
    "RC_Keychain_1140_Black": {
        "name-1": {
            "x": 292,
            "y": 543,
            "angle": 329,
            "maxWidth": 253,
            "height": 55,
            "fontSize": 24
        }
    },
    "RC_Keychain_1139": {
        "name-1": {
            "x": 501,
            "y": 506,
            "angle": 0,
            "maxWidth": 317,
            "height": 69,
            "fontSize": 30
        },
        "extra-1": {
            "x": 512,
            "y": 898,
            "angle": 0,
            "maxWidth": 260,
            "height": 54,
            "fontSize": 24
        }
    },
    "RC_Keychain_1138": {
        "name-1": {
            "x": 532,
            "y": 538,
            "angle": 0,
            "maxWidth": 271,
            "height": 59,
            "fontSize": 24
        },
        "extra-1": {
            "x": 545,
            "y": 963,
            "angle": 0,
            "maxWidth": 276,
            "height": 57,
            "fontSize": 24
        }
    },
    "RC_Keychain_1137": {
        "name-1": {
            "x": 507,
            "y": 562,
            "angle": 0,
            "maxWidth": 260,
            "height": 56,
            "fontSize": 25
        },
        "extra-1": {
            "x": 510,
            "y": 900,
            "angle": 0,
            "maxWidth": 260,
            "height": 54,
            "fontSize": 24
        }
    },
    "RC_Keychain_1136": {
        "name-1": {
            "x": 530,
            "y": 744,
            "angle": 0,
            "maxWidth": 354,
            "height": 77,
            "fontSize": 32
        }
    },
    "RC_Keychain_1135": {
        "name-1": {
            "x": 510,
            "y": 538,
            "angle": 0,
            "maxWidth": 334,
            "height": 72,
            "fontSize": 32
        },
        "extra-1": {
            "x": 504,
            "y": 836,
            "angle": 0,
            "maxWidth": 260,
            "height": 54,
            "fontSize": 24
        }
    },
    "RC_Keychain_1134": {
        "name-1": {
            "x": 496,
            "y": 522,
            "angle": 0,
            "maxWidth": 187,
            "height": 40,
            "fontSize": 18
        }
    },
    "RC_Keychain_1133": {
        "name-1": {
            "x": 493,
            "y": 753,
            "angle": 0,
            "maxWidth": 254,
            "height": 55,
            "fontSize": 24
        }
    },
    "RC_Keychain_1132_black": {
        "name-1": {
            "x": 476,
            "y": 698,
            "angle": 88,
            "maxWidth": 334,
            "height": 72,
            "fontSize": 32
        }
    },
    "RC_Keychain_1131": {
        "name-1": {
            "x": 521,
            "y": 499,
            "angle": 0,
            "maxWidth": 257,
            "height": 56,
            "fontSize": 25
        }
    },
    "RC_Keychain_1130": {
        "name-1": {
            "x": 525,
            "y": 512,
            "angle": 0,
            "maxWidth": 244,
            "height": 53,
            "fontSize": 23
        }
    },
    
    # Batch 2
    "RC_Keychain_1129": {
        "name-1": {
            "x": 338,
            "y": 520,
            "angle": 0,
            "maxWidth": 206,
            "height": 45,
            "fontSize": 20
        },
        "extra-2": {
            "x": 256,
            "y": 405,
            "angle": 334,
            "maxWidth": 162,
            "height": 63,
            "fontSize": 28
        }
    },
    "RC_Keychain_1128": {
        "name-1": {
            "x": 622,
            "y": 676,
            "angle": 69,
            "maxWidth": 334,
            "height": 72,
            "fontSize": 32
        }
    },
    "RC_Keychain_1127": {
        "name-1": {
            "x": 596,
            "y": 664,
            "angle": 70,
            "maxWidth": 334,
            "height": 72,
            "fontSize": 32
        }
    },
    "RC_Keychain_1126": {
        "name-1": {
            "x": 536,
            "y": 654,
            "angle": 72,
            "maxWidth": 334,
            "height": 72,
            "fontSize": 32
        }
    },
    "RC_Keychain_1125": {
        "name-1": {
            "x": 626,
            "y": 684,
            "angle": 71,
            "maxWidth": 334,
            "height": 72,
            "fontSize": 32
        }
    },
    "RC_Keychain_1124": {
        "name-1": {
            "x": 622,
            "y": 552,
            "angle": 53,
            "maxWidth": 334,
            "height": 72,
            "fontSize": 32
        }
    },
    "RC_Keychain_1123": {
        "name-1": {
            "x": 582,
            "y": 546,
            "angle": 50,
            "maxWidth": 334,
            "height": 72,
            "fontSize": 32
        }
    },
    "RC_Keychain_1122": {
        "name-1": {
            "x": 606,
            "y": 597,
            "angle": 48,
            "maxWidth": 202,
            "height": 44,
            "fontSize": 19
        }
    },
    "RC_Keychain_1121": {
        "name-1": {
            "x": 618,
            "y": 633,
            "angle": 50,
            "maxWidth": 243,
            "height": 53,
            "fontSize": 23
        }
    },
    "RC_Keychain_1120": {
        "name-1": {
            "x": 644,
            "y": 656,
            "angle": 48,
            "maxWidth": 224,
            "height": 48,
            "fontSize": 21
        }
    },
    "RC_Keychain_1119": {
        "name-1": {
            "x": 593,
            "y": 661,
            "angle": 46,
            "maxWidth": 238,
            "height": 51,
            "fontSize": 23
        }
    },
    "RC_Keychain_1118": {
        "name-1": {
            "x": 280,
            "y": 443,
            "angle": 48,
            "maxWidth": 234,
            "height": 51,
            "fontSize": 22
        }
    },
    "RC_Keychain_1117": {
        "name-1": {
            "x": 311,
            "y": 404,
            "angle": 49,
            "maxWidth": 217,
            "height": 47,
            "fontSize": 21
        }
    },
    "RC_Keychain_1116": {
        "name-1": {
            "x": 289,
            "y": 424,
            "angle": 47,
            "maxWidth": 239,
            "height": 52,
            "fontSize": 23
        }
    },
    "RC_Keychain_1115": {
        "name-1": {
            "x": 285,
            "y": 425,
            "angle": 51,
            "maxWidth": 238,
            "height": 52,
            "fontSize": 23
        }
    },
    "RC_Keychain_1114": {
        "name-1": {
            "x": 536,
            "y": 640,
            "angle": 325,
            "maxWidth": 219,
            "height": 47,
            "fontSize": 21
        }
    },
    "RC_Keychain_1113": {
        "name-1": {
            "x": 595,
            "y": 586,
            "angle": 315,
            "maxWidth": 215,
            "height": 46,
            "fontSize": 21
        }
    },
    "RC_Keychain_1112": {
        "name-1": {
            "x": 618,
            "y": 634,
            "angle": 52,
            "maxWidth": 334,
            "height": 72,
            "fontSize": 32
        }
    },
    "RC_Keychain_1111": {
        "name-1": {
            "x": 672,
            "y": 786,
            "angle": 0,
            "maxWidth": 334,
            "height": 72,
            "fontSize": 32
        }
    },
    "RC_Keychain_1110": {
        "name-1": {
            "x": 508,
            "y": 788,
            "angle": 0,
            "maxWidth": 334,
            "height": 72,
            "fontSize": 32
        }
    },
    "RC_Keychain_1109": {
        "name-1": {
            "x": 520,
            "y": 794,
            "angle": 0,
            "maxWidth": 334,
            "height": 72,
            "fontSize": 32
        }
    },
    "RC_Keychain_1108": {
        "name-1": {
            "x": 498,
            "y": 702,
            "angle": 91,
            "maxWidth": 334,
            "height": 72,
            "fontSize": 32
        }
    },
    "RC_Keychain_1107": {
        "name-1": {
            "x": 506,
            "y": 706,
            "angle": 91,
            "maxWidth": 334,
            "height": 72,
            "fontSize": 32
        }
    },
    "RC_Keychain_1106": {
        "name-1": {
            "x": 540,
            "y": 668,
            "angle": 0,
            "maxWidth": 334,
            "height": 72,
            "fontSize": 32
        }
    },
    "RC_Keychain_1105": {
        "name-1": {
            "x": 485,
            "y": 656,
            "angle": 276,
            "maxWidth": 310,
            "height": 67,
            "fontSize": 30
        }
    },
    "RC_Keychain_1104": {
        "name-1": {
            "x": 470,
            "y": 642,
            "angle": 0,
            "maxWidth": 334,
            "height": 72,
            "fontSize": 32
        }
    },
    "RC_Keychain_1103": {
        "name-1": {
            "x": 442,
            "y": 756,
            "angle": 288,
            "maxWidth": 334,
            "height": 72,
            "fontSize": 32
        }
    },
    "RC_Keychain_1102": {
        "name-1": {
            "x": 458,
            "y": 708,
            "angle": 0,
            "maxWidth": 334,
            "height": 72,
            "fontSize": 32
        }
    },
    "RC_Keychain_1101": {
        "name-1": {
            "x": 530,
            "y": 700,
            "angle": 267,
            "maxWidth": 334,
            "height": 72,
            "fontSize": 32
        }
    }
}

def update_keychains():
    json_path = os.path.join(
        os.path.dirname(os.path.abspath(__file__)),
        '..',
        'frontend',
        'src',
        'data',
        'customization.json'
    )
    
    if not os.path.exists(json_path):
        print(f"[ERROR] customization.json not found at {json_path}")
        return
        
    with open(json_path, 'r') as f:
        data = json.load(f)
        
    existing_slugs = {item.get('slug') for item in data if item.get('slug')}
    
    # 1. Export missing target keychains from DB to json data structure
    new_exports = 0
    for slug in TARGETS.keys():
        if slug not in existing_slugs:
            try:
                product = Product.objects.get(slug=slug)
                entry = {
                    "productId": product.id,
                    "productName": product.name,
                    "slug": product.slug,
                    "baseImage": product.image,
                    "zones": json.loads(product.customization_config) if product.customization_config else []
                }
                data.append(entry)
                existing_slugs.add(slug)
                new_exports += 1
                print(f"[INFO] Exported {slug} from DB to JSON list")
            except Product.DoesNotExist:
                print(f"[WARNING] Product slug {slug} not found in Django DB!")
                
    if new_exports > 0:
        print(f"[SUCCESS] Exported {new_exports} missing products to customization.json array")

    # 2. Update zones coordinates in JSON data structure
    updated_products = []
    
    for item in data:
        slug = item.get('slug')
        if slug in TARGETS:
            target_zones = TARGETS[slug]
            updated_zones = []
            
            # Map zones list
            zones = item.get('zones', [])
            for zone_id, new_coords in target_zones.items():
                # Find matching zone
                zone_found = False
                for zone in zones:
                    if zone.get('id') == zone_id:
                        # Update only mapped keys
                        for k, v in new_coords.items():
                            zone[k] = v
                        zone_found = True
                        updated_zones.append(zone_id)
                        break
                        
                # If not found, create new zone object (should not happen normally)
                if not zone_found:
                    new_zone = {
                        "id": zone_id,
                        "type": "text",
                        "originX": "center",
                        "originY": "center",
                        "fontFamily": "Inter, sans-serif",
                        "fill": "#000000",
                        "opacity": 1.0,
                        "placeholder": "Your Name" if zone_id == "name-1" else "Extra Text"
                    }
                    for k, v in new_coords.items():
                        new_zone[k] = v
                    zones.append(new_zone)
                    updated_zones.append(zone_id)
            
            item['zones'] = zones
            updated_products.append((slug, updated_zones))
            
    # 3. Save customization.json with pretty formatting
    with open(json_path, 'w') as f:
        json.dump(data, f, indent=2)
    print(f"\n[SUCCESS] customization.json saved successfully at {json_path}")
    
    # 4. Run the DB synchronization
    print("\nSyncing changes to SQLite database...")
    sync_customization_zones()
    print("[SUCCESS] SQLite database sync completed successfully!\n")
    
    # 5. Print confirmation summary
    print("=" * 60)
    print("VERIFICATION SUMMARY:")
    print("=" * 60)
    for slug, zones in updated_products:
        print(f"Product Slug: {slug}")
        print(f"  Updated Zones: {', '.join(zones)}")
        print("  Coordinates applied:")
        for z_id in zones:
            print(f"    - {z_id}: {TARGETS[slug][z_id]}")
    print("-" * 60)
    print("Total updated products:", len(updated_products))
    print("=" * 60)

if __name__ == '__main__':
    update_keychains()
