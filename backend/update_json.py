import os
import sys
import json
import django

sys.path.append(os.path.dirname(os.path.abspath(__file__)))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'core.settings')
django.setup()

from products.models import Product

updates = {
  731: {"create": {2: {"placeholder": "Text"}}, "zones": {1: {"x": 421, "y": 787, "angle": 0}, 2: {"x": 677, "y": 679, "angle": 0}}},
  732: {"create": {2: {"placeholder": "Text"}}, "zones": {1: {"x": 417, "y": 788, "angle": 0}, 2: {"x": 668, "y": 672, "angle": 0}}},
  733: {"create": {2: {"placeholder": "Text"}}, "zones": {1: {"x": 459, "y": 768, "angle": 0}, 2: {"x": 678, "y": 667, "angle": 0}}},
  734: {"create": {2: {"placeholder": "Text"}}, "zones": {1: {"x": 481, "y": 786, "angle": 0}, 2: {"x": 698, "y": 649, "angle": 0}}},
  735: {"create": {2: {"placeholder": "Text"}}, "zones": {1: {"x": 461, "y": 773, "angle": 0}, 2: {"x": 691, "y": 679, "angle": 0}}},
  736: {"create": {2: {"placeholder": "Text"}}, "zones": {1: {"x": 415, "y": 805, "angle": 0}, 2: {"x": 695, "y": 673, "angle": 0}}},
  737: {"create": {2: {"placeholder": "Text"}}, "zones": {1: {"x": 430, "y": 775, "angle": 0}, 2: {"x": 714, "y": 667, "angle": 0}}},
  738: {"create": {2: {"placeholder": "Text"}}, "zones": {1: {"x": 459, "y": 770, "angle": 0}, 2: {"x": 711, "y": 660, "angle": 0}}},
  739: {"create": {2: {"placeholder": "Text"}}, "zones": {1: {"x": 251, "y": 798, "angle": 0}, 2: {"x": 701, "y": 682, "angle": 0}}},
  
  740: {"zones": {1: {"x": 642, "y": 652, "angle": 0}}},
  741: {"zones": {1: {"x": 552, "y": 778, "angle": 20}}},
  742: {"zones": {1: {"x": 533, "y": 390, "angle": 342}}},
  743: {"zones": {1: {"x": 494, "y": 820, "angle": 0}}},
  744: {"zones": {1: {"x": 502, "y": 612, "angle": 280}}},
  745: {"zones": {1: {"x": 500, "y": 535, "angle": 317}}},
  746: {"zones": {1: {"x": 443, "y": 537, "angle": 313}}},
  747: {"zones": {1: {"x": 499, "y": 491, "angle": 316}}},
  748: {"zones": {1: {"x": 489, "y": 542, "angle": 269}}},
  749: {"zones": {1: {"x": 429, "y": 838, "angle": 0}}},
  750: {"zones": {1: {"x": 451, "y": 803, "angle": 0}}},
  751: {"zones": {1: {"x": 531, "y": 837, "angle": 0}}},
  752: {"zones": {1: {"x": 440, "y": 792, "angle": 0}}},
  753: {"zones": {1: {"x": 430, "y": 805, "angle": 0}}},
  754: {"zones": {1: {"x": 585, "y": 793, "angle": 0}}},
  755: {"zones": {1: {"x": 406, "y": 813, "angle": 0}}},

  756: {"create": {2: {"placeholder": "Text"}}, "zones": {1: {"x": 263, "y": 546, "angle": 90}, 2: {"x": 715, "y": 563, "angle": 90}}},
  757: {"create": {2: {"placeholder": "Text"}}, "zones": {1: {"x": 247, "y": 632, "angle": 89}, 2: {"x": 701, "y": 622, "angle": 89}}},
  758: {"create": {2: {"placeholder": "Text"}}, "zones": {1: {"x": 259, "y": 664, "angle": 91}, 2: {"x": 669, "y": 582, "angle": 359}}},
  759: {"create": {2: {"placeholder": "Text"}}, "zones": {1: {"x": 277, "y": 671, "angle": 92}, 2: {"x": 671, "y": 590, "angle": 360}}},

  760: {"create": {2: {"placeholder": "Pen Text"}, 3: {"placeholder": "Cardholder"}, 4: {"placeholder": "Text"}},
        "zones": {1: {"x": 310, "y": 622, "angle": 46}, 2: {"x": 554, "y": 470, "angle": 43}, 3: {"x": 791, "y": 427, "angle": 327}, 4: {"x": 570, "y": 276, "angle": 327}}},

  761: {"create": {2: {"placeholder": "Pen Text"}}, "zones": {1: {"x": 320, "y": 627, "angle": 92}, 2: {"x": 725, "y": 559, "angle": 88}}},
  762: {"create": {2: {"placeholder": "Pen Text"}}, "zones": {2: {"x": 702, "y": 513, "angle": 269}}},
  763: {"create": {2: {"placeholder": "Pen Text"}}, "zones": {2: {"x": 195, "y": 610, "angle": 269}}},
  764: {"create": {2: {"placeholder": "Pen Text"}}, "zones": {1: {"x": 781, "y": 648, "angle": 270}, 2: {"x": 168, "y": 619, "angle": 270}}},
  765: {"create": {2: {"placeholder": "Pen Text"}}, "zones": {1: {"x": 771, "y": 614, "angle": 270}, 2: {"x": 198, "y": 583, "angle": 270}}},

  766: {"zones": {1: {"x": 606, "y": 815, "angle": 350}}},
  767: {"zones": {1: {"x": 481, "y": 891, "angle": 5}}},
  768: {"zones": {1: {"x": 232, "y": 487, "angle": 0}}},
  769: {"zones": {1: {"x": 371, "y": 611, "angle": 313}}},
  770: {"zones": {1: {"x": 441, "y": 509, "angle": 0}}},
  771: {},
  772: {"zones": {1: {"x": 501, "y": 526, "angle": 270}}},
  773: {},
  774: {"zones": {1: {"x": 497, "y": 639, "angle": 275}}},
  775: {"zones": {1: {"x": 491, "y": 513, "angle": 271}}},
  776: {"zones": {1: {"x": 501, "y": 506, "angle": 270}}},
  777: {"zones": {1: {"x": 499, "y": 509, "angle": 269}}},

  786: {"zones": {1: {"x": 525, "y": 706, "angle": 339}}},
  787: {"zones": {1: {"x": 763, "y": 533, "angle": 351}}},

  789: {"remove_by_name": "extra text", "zones": {1: {"x": 311, "y": 855, "angle": 0}}},
  790: {"remove_by_name": "extra text", "zones": {1: {"x": 510, "y": 624, "angle": 12}}},
  791: {"remove_by_name": "extra text", "zones": {1: {"x": 186, "y": 658, "angle": 12}}},
  792: {"remove_by_name": "extra text", "zones": {1: {"x": 486, "y": 893, "angle": 360}}},
  793: {"remove_by_name": "extra text", "zones": {1: {"x": 381, "y": 448, "angle": 122}}},
  794: {"remove_by_name": "extra text", "zones": {1: {"x": 611, "y": 502, "angle": 305}}},
  795: {"remove_by_name": "extra text", "zones": {1: {"x": 509, "y": 655, "angle": 0}}},
  796: {"remove_by_name": "extra text", "zones": {1: {"x": 514, "y": 649, "angle": 0}}},
  797: {"remove_by_name": "extra text", "zones": {1: {"x": 532, "y": 649, "angle": 0}}},
  798: {"remove_by_name": "extra text", "zones": {1: {"x": 592, "y": 649, "angle": 353}}},
  799: {"remove_by_name": "extra text", "zones": {1: {"x": 525, "y": 650, "angle": 0}}},
  800: {"remove_by_name": "extra text", "zones": {1: {"x": 468, "y": 839, "angle": 7}}},
  801: {"remove_by_name": "extra text", "zones": {1: {"x": 178, "y": 439, "angle": 0}}},
  802: {"remove_by_name": "extra text", "zones": {1: {"x": 221, "y": 404, "angle": 0}}},
  803: {"remove_by_name": "extra text", "zones": {1: {"x": 179, "y": 459, "angle": 358}}},
  804: {"remove_by_name": "extra text", "zones": {1: {"x": 498, "y": 861, "angle": 0}}},
  805: {"remove_by_name": "extra text", "zones": {1: {"x": 515, "y": 776, "angle": 0}}},
  806: {"remove_by_name": "extra text", "zones": {1: {"x": 527, "y": 813, "angle": 89}}},
  807: {"remove_by_name": "extra text", "zones": {1: {"x": 169, "y": 450, "angle": 145}}},
  808: {"remove_by_name": "extra text", "zones": {1: {"x": 782, "y": 854, "angle": 352}}},
  809: {"remove_by_name": "extra text", "zones": {1: {"x": 419, "y": 584, "angle": 270}}},
  810: {"remove_by_name": "extra text", "zones": {1: {"x": 383, "y": 876, "angle": 271}}},
  811: {"remove_by_name": "extra text", "zones": {1: {"x": 383, "y": 759, "angle": 270}}},
  812: {"remove_by_name": "extra text", "zones": {1: {"x": 436, "y": 795, "angle": 270}}},
  813: {"remove_by_name": "extra text", "zones": {1: {"x": 444, "y": 719, "angle": 269}}},
  814: {"remove_by_name": "extra text", "zones": {1: {"x": 416, "y": 783, "angle": 269}}},
  815: {"remove_by_name": "extra text", "zones": {1: {"x": 416, "y": 812, "angle": 270}}},
  816: {"remove_by_name": "extra text", "zones": {1: {"x": 422, "y": 804, "angle": 271}}},
  817: {"remove_by_name": "extra text", "zones": {1: {"x": 430, "y": 778, "angle": 270}}},
  818: {"remove_by_name": "extra text", "zones": {1: {"x": 525, "y": 767, "angle": 357}}},
  819: {"remove_by_name": "extra text", "zones": {1: {"x": 447, "y": 653, "angle": 270}}},
  820: {"remove_by_name": "extra text", "zones": {1: {"x": 428, "y": 710, "angle": 271}}},
  821: {"remove_by_name": "extra text", "zones": {1: {"x": 449, "y": 793, "angle": 271}}},
  822: {"remove_by_name": "extra text", "zones": {1: {"x": 414, "y": 807, "angle": 270}}},
  823: {"remove_by_name": "extra text", "zones": {1: {"x": 386, "y": 805, "angle": 270}}},
  824: {"remove_by_name": "extra text", "zones": {1: {"x": 398, "y": 860, "angle": 270}}},
  825: {"remove_by_name": "extra text", "zones": {1: {"x": 451, "y": 654, "angle": 269}}},

  826: {"create": {3: {"placeholder": "cup2 Text"}}, "zones": {1: {"placeholder": "Bottle Text", "x": 386, "y": 747, "angle": 272}, 2: {"placeholder": "Cup1 Text", "x": 624, "y": 329, "angle": 270}}},
  
  827: {"remove_by_name": "extra text", "zones": {1: {"x": 435, "y": 740, "angle": 269}}},
  828: {"remove_by_name": "extra text", "zones": {1: {"x": 441, "y": 747, "angle": 270}}},
  829: {"remove_by_name": "extra text", "zones": {1: {"x": 446, "y": 768, "angle": 270}}}
}

json_path = os.path.join(
    os.path.dirname(os.path.dirname(os.path.abspath(__file__))),
    'frontend',
    'src',
    'data',
    'customization.json'
)

with open(json_path, 'r', encoding='utf-8') as f:
    customization_data = json.load(f)

slug_to_index = {item.get('slug'): i for i, item in enumerate(customization_data) if item.get('slug')}

for db_id, data in updates.items():
    try:
        product = Product.all_objects.get(id=db_id)
        slug = product.slug
        if slug in slug_to_index:
            idx = slug_to_index[slug]
            item = customization_data[idx]
            zones = item.get('zones', [])
            
            if 'zones' in data:
                for z_idx_str, z_data in data['zones'].items():
                    z_idx = int(z_idx_str) - 1
                    if z_idx < len(zones):
                        for k, v in z_data.items():
                            zones[z_idx][k] = v
                            
            if 'create' in data:
                for z_idx_str, props in data['create'].items():
                    z_idx = int(z_idx_str) - 1
                    if len(zones) <= z_idx:
                        while len(zones) <= z_idx:
                            new_zone = {
                                "id": f"text-zone-{len(zones)+1}",
                                "type": "text",
                                "x": 500,
                                "y": 500,
                                "originX": "center",
                                "originY": "center",
                                "angle": 0,
                                "maxWidth": 400,
                                "maxChars": 15,
                                "fontFamily": "Inter, sans-serif",
                                "fontSize": 12,
                                "minFontSize": 10,
                                "fill": "#000000",
                                "opacity": 1.0,
                                "placeholder": "Text"
                            }
                            zones.append(new_zone)
                        for k, v in props.items():
                            zones[z_idx][k] = v
                    else:
                        for k, v in props.items():
                            zones[z_idx][k] = v
            
            if 'replace_by_name' in data:
                for old_name, new_name in data['replace_by_name'].items():
                    for z in zones:
                        if old_name.lower() in z.get('placeholder', '').lower():
                            z['placeholder'] = new_name
                            
            if 'remove_by_name' in data:
                name_to_remove = data['remove_by_name'].lower()
                new_zones = []
                for z in zones:
                    if name_to_remove not in z.get('placeholder', '').lower():
                        new_zones.append(z)
                zones = new_zones
                item['zones'] = zones
            
            if 'remove' in data and data['remove']:
                new_zones = [z for i, z in enumerate(zones) if (i+1) not in data['remove']]
                item['zones'] = new_zones
                zones = new_zones
                
            print(f"Updated product ID {db_id} (slug: {slug})")
        else:
            print(f"Slug {slug} for product ID {db_id} not found in customization.json")
    except Product.DoesNotExist:
        print(f"Product ID {db_id} not found in DB")

with open(json_path, 'w', encoding='utf-8') as f:
    json.dump(customization_data, f, indent=2)

print("Finished updating customization.json")
