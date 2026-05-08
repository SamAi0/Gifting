import json
import os
from django.conf import settings

_MAHARASHTRA_PINCODES = None

def get_maharashtra_pincodes():
    global _MAHARASHTRA_PINCODES
    if _MAHARASHTRA_PINCODES is None:
        json_path = os.path.join(settings.BASE_DIR, 'orders', 'data', 'maharashtra_pincodes.json')
        try:
            with open(json_path, 'r') as f:
                pincode_list = json.load(f)
                _MAHARASHTRA_PINCODES = set(str(p) for p in pincode_list)
        except Exception as e:
            print(f"Error loading Maharashtra pincodes: {e}")
            _MAHARASHTRA_PINCODES = set()
    return _MAHARASHTRA_PINCODES

def is_maharashtra_pincode(pincode):
    valid_set = get_maharashtra_pincodes()
    # Simple check for now: if list is small, we also check prefixes for demo/safety
    # But strictly speaking, it should be in the set if it's production grade.
    return str(pincode).strip() in valid_set
