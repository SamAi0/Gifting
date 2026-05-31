import os
import sys
import json
import re
import django

# Setup Django settings
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'core.settings')
django.setup()

from products.models import Product

WORKSPACE_DIR = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
FRONTEND_JSON_PATH = os.path.join(WORKSPACE_DIR, 'frontend', 'src', 'data', 'customization.json')

RAW_LOGS = """
product id : 321
CanvasCustomizer.jsx:115  Zone Update [zone-321-1] 
CanvasCustomizer.jsx:116 "x": 227, "y": 321, "angle": 270
CanvasCustomizer.jsx:117 --------------------------
CanvasCustomizer.jsx:115  Zone Update [zone-321-2] 
CanvasCustomizer.jsx:116 "x": 318, "y": 231, "angle": 268
CanvasCustomizer.jsx:117 --------------------------
CanvasCustomizer.jsx:115  Zone Update [zone-321-3] 
CanvasCustomizer.jsx:116 "x": 336, "y": 434, "angle": 0


product id : 322
CanvasCustomizer.jsx:115  Zone Update [zone-322-1] 
CanvasCustomizer.jsx:116 "x": 240, "y": 356, "angle": 246
CanvasCustomizer.jsx:117 --------------------------
CanvasCustomizer.jsx:115  Zone Update [zone-322-2] 
CanvasCustomizer.jsx:116 "x": 427, "y": 375, "angle": 0
CanvasCustomizer.jsx:117 --------------------------



product id :323

CanvasCustomizer.jsx:115  Zone Update [zone-323-1] 
CanvasCustomizer.jsx:116 "x": 217, "y": 340, "angle": 270
CanvasCustomizer.jsx:117 --------------------------
CanvasCustomizer.jsx:115  Zone Update [zone-323-2] 
CanvasCustomizer.jsx:116 "x": 337, "y": 398, "angle": 0
CanvasCustomizer.jsx:117 --------------------------


product id :324
CanvasCustomizer.jsx:115  Zone Update [zone-324-1] 
CanvasCustomizer.jsx:116 "x": 213, "y": 329, "angle": 271
CanvasCustomizer.jsx:117 --------------------------
CanvasCustomizer.jsx:115  Zone Update [zone-324-2] 
CanvasCustomizer.jsx:116 "x": 313, "y": 332, "angle": 269
CanvasCustomizer.jsx:117 --------------------------

product id :325
CanvasCustomizer.jsx:115  Zone Update [zone-325-1] 
CanvasCustomizer.jsx:116 "x": 217, "y": 298, "angle": 271
CanvasCustomizer.jsx:117 --------------------------
CanvasCustomizer.jsx:115  Zone Update [zone-325-2] 
CanvasCustomizer.jsx:116 "x": 314, "y": 329, "angle": 270
CanvasCustomizer.jsx:117 --------------------------


product id :326
CanvasCustomizer.jsx:115  Zone Update [zone-326-1] 
CanvasCustomizer.jsx:116 "x": 213, "y": 306, "angle": 271
CanvasCustomizer.jsx:117 --------------------------
CanvasCustomizer.jsx:115  Zone Update [zone-326-2] 
CanvasCustomizer.jsx:116 "x": 307, "y": 321, "angle": 271
CanvasCustomizer.jsx:117 --------------------------
CanvasCustomizer.jsx:115  Zone Update [zone-326-3] 
CanvasCustomizer.jsx:116 "x": 318, "y": 409, "angle": 0
CanvasCustomizer.jsx:117 --------------------------


product id :327

CanvasCustomizer.jsx:115  Zone Update [zone-327-1] 
CanvasCustomizer.jsx:116 "x": 215, "y": 318, "angle": 269
CanvasCustomizer.jsx:117 --------------------------
CanvasCustomizer.jsx:115  Zone Update [zone-327-1] 
CanvasCustomizer.jsx:116 "x": 216, "y": 327, "angle": 269
CanvasCustomizer.jsx:117 --------------------------
CanvasCustomizer.jsx:115  Zone Update [zone-327-2] 
CanvasCustomizer.jsx:116 "x": 313, "y": 328, "angle": 270

product id :328
CanvasCustomizer.jsx:115  Zone Update [zone-328-1] 
CanvasCustomizer.jsx:116 "x": 219, "y": 333, "angle": 269
CanvasCustomizer.jsx:117 --------------------------
CanvasCustomizer.jsx:115  Zone Update [zone-328-2] 
CanvasCustomizer.jsx:116 "x": 309, "y": 328, "angle": 269
CanvasCustomizer.jsx:117 --------------------------

product id :329
--------------------------
CanvasCustomizer.jsx:115  Zone Update [zone-329-1] 
CanvasCustomizer.jsx:116 "x": 215, "y": 317, "angle": 271
CanvasCustomizer.jsx:117 --------------------------
CanvasCustomizer.jsx:115  Zone Update [zone-329-2] 
CanvasCustomizer.jsx:116 "x": 309, "y": 323, "angle": 269
CanvasCustomizer.jsx:117 --------------------------


product id :330
--------------------------
CanvasCustomizer.jsx:115  Zone Update [zone-330-1] 
CanvasCustomizer.jsx:116 "x": 99, "y": 81, "angle": 0
CanvasCustomizer.jsx:117 --------------------------
CanvasCustomizer.jsx:115  Zone Update [zone-330-2] 
CanvasCustomizer.jsx:116 "x": 225, "y": 164, "angle": 270
CanvasCustomizer.jsx:117 --------------------------



product id :331
--------------------------
CanvasCustomizer.jsx:115  Zone Update [zone-331-1] 
CanvasCustomizer.jsx:116 "x": 118, "y": 88, "angle": 0
CanvasCustomizer.jsx:117 --------------------------
CanvasCustomizer.jsx:115  Zone Update [zone-331-2] 
CanvasCustomizer.jsx:116 "x": 237, "y": 155, "angle": 272
CanvasCustomizer.jsx:117 --------------------------
CanvasCustomizer.jsx:115  Zone Update [zone-331-3] 
CanvasCustomizer.jsx:116 "x": 278, "y": 246, "angle": 0
CanvasCustomizer.jsx:117 --------------------------
CanvasCustomizer.jsx:115  Zone Update [zone-331-4] 
CanvasCustomizer.jsx:116 "x": 278, "y": 282, "angle": 0
CanvasCustomizer.jsx:117 --------------------------
CanvasCustomizer.jsx:115  Zone Update [zone-331-5] 
CanvasCustomizer.jsx:116 "x": 274, "y": 318, "angle": 0


product id :332
--------------------------
CanvasCustomizer.jsx:115  Zone Update [zone-332-1] 
CanvasCustomizer.jsx:116 "x": 126, "y": 87, "angle": 0
CanvasCustomizer.jsx:117 --------------------------
CanvasCustomizer.jsx:115  Zone Update [zone-332-2] 
CanvasCustomizer.jsx:116 "x": 247, "y": 171, "angle": 269
CanvasCustomizer.jsx:117 --------------------------
CanvasCustomizer.jsx:115  Zone Update [zone-332-3] 
CanvasCustomizer.jsx:116 "x": 277, "y": 281, "angle": 0
CanvasCustomizer.jsx:117 --------------------------
CanvasCustomizer.jsx:115  Zone Update [zone-332-4] 
CanvasCustomizer.jsx:116 "x": 276, "y": 307, "angle": 0
CanvasCustomizer.jsx:117 --------------------------
CanvasCustomizer.jsx:115  Zone Update [zone-332-5] 
CanvasCustomizer.jsx:116 "x": 277, "y": 333, "angle": 0
CanvasCustomizer.jsx:117 --------------------------

product id :333
--------------------------
CanvasCustomizer.jsx:115  Zone Update [zone-333-1] 
CanvasCustomizer.jsx:116 "x": 107, "y": 155, "angle": 271
CanvasCustomizer.jsx:117 --------------------------
CanvasCustomizer.jsx:115  Zone Update [zone-333-2] 
CanvasCustomizer.jsx:116 "x": 244, "y": 98, "angle": 0
CanvasCustomizer.jsx:117 --------------------------
CanvasCustomizer.jsx:115  Zone Update [zone-333-3] 
CanvasCustomizer.jsx:116 "x": 277, "y": 225, "angle": 0
CanvasCustomizer.jsx:117 --------------------------
CanvasCustomizer.jsx:115  Zone Update [zone-333-4] 
CanvasCustomizer.jsx:116 "x": 277, "y": 266, "angle": 0
CanvasCustomizer.jsx:117 --------------------------
CanvasCustomizer.jsx:115  Zone Update [zone-333-5] 
CanvasCustomizer.jsx:116 "x": 275, "y": 314, "angle": 0

product id :334
-------------------------
CanvasCustomizer.jsx:115  Zone Update [zone-334-1] 
CanvasCustomizer.jsx:116 "x": 115, "y": 67, "angle": 0
CanvasCustomizer.jsx:117 --------------------------
CanvasCustomizer.jsx:115  Zone Update [zone-334-2] 
CanvasCustomizer.jsx:116 "x": 249, "y": 155, "angle": 270
CanvasCustomizer.jsx:117 --------------------------
CanvasCustomizer.jsx:115  Zone Update [zone-334-3] 
CanvasCustomizer.jsx:116 "x": 273, "y": 306, "angle": 0
CanvasCustomizer.jsx:117 --------------------------
CanvasCustomizer.jsx:115  Zone Update [zone-334-4] 
CanvasCustomizer.jsx:116 "x": 274, "y": 327, "angle": 0
CanvasCustomizer.jsx:117 --------------------------
CanvasCustomizer.jsx:115  Zone Update [zone-334-5] 
CanvasCustomizer.jsx:116 "x": 274, "y": 352, "angle": 0
CanvasCustomizer.jsx:117 --------------------------

product id :335
--------------------------
CanvasCustomizer.jsx:115  Zone Update [zone-335-1] 
CanvasCustomizer.jsx:116 "x": 303, "y": 41, "angle": 0
CanvasCustomizer.jsx:117 --------------------------
CanvasCustomizer.jsx:115  Zone Update [zone-335-2] 
CanvasCustomizer.jsx:116 "x": 427, "y": 131, "angle": 272
CanvasCustomizer.jsx:117 --------------------------
CanvasCustomizer.jsx:115  Zone Update [zone-335-3] 
CanvasCustomizer.jsx:116 "x": 301, "y": 175, "angle": 0
CanvasCustomizer.jsx:117 --------------------------
CanvasCustomizer.jsx:115  Zone Update [zone-335-5] 
CanvasCustomizer.jsx:116 "x": 301, "y": 205, "angle": 0
CanvasCustomizer.jsx:117 --------------------------
CanvasCustomizer.jsx:115  Zone Update [zone-335-4] 
CanvasCustomizer.jsx:116 "x": 302, "y": 233, "angle": 0


product id :336
--------------------------
CanvasCustomizer.jsx:115  Zone Update [zone-336-1] 
CanvasCustomizer.jsx:116 "x": 84, "y": 73, "angle": 0
CanvasCustomizer.jsx:117 --------------------------
CanvasCustomizer.jsx:115  Zone Update [zone-336-2] 
CanvasCustomizer.jsx:116 "x": 186, "y": 150, "angle": 269
CanvasCustomizer.jsx:117 --------------------------
CanvasCustomizer.jsx:115  Zone Update [zone-336-3] 
CanvasCustomizer.jsx:116 "x": 77, "y": 183, "angle": 0
CanvasCustomizer.jsx:117 --------------------------
CanvasCustomizer.jsx:115  Zone Update [zone-336-4] 
CanvasCustomizer.jsx:116 "x": 75, "y": 200, "angle": 0
CanvasCustomizer.jsx:117 --------------------------
CanvasCustomizer.jsx:115  Zone Update [zone-336-5] 
CanvasCustomizer.jsx:116 "x": 77, "y": 217, "angle": 0
CanvasCustomizer.jsx:117 --------------------------


 
product id :337
--------------------------
CanvasCustomizer.jsx:115  Zone Update [zone-337-1] 
CanvasCustomizer.jsx:116 "x": 286, "y": 153, "angle": 0
CanvasCustomizer.jsx:117 --------------------------
CanvasCustomizer.jsx:115  Zone Update [zone-337-2] 
CanvasCustomizer.jsx:116 "x": 276, "y": 423, "angle": 0
CanvasCustomizer.jsx:117 --------------------------
CanvasCustomizer.jsx:115  Zone Update [zone-337-3] 
CanvasCustomizer.jsx:116 "x": 273, "y": 484, "angle": 0
CanvasCustomizer.jsx:117 --------------------------
CanvasCustomizer.jsx:115  Zone Update [zone-337-5] 
CanvasCustomizer.jsx:116 "x": 276, "y": 576, "angle": 0
CanvasCustomizer.jsx:117 --------------------------
CanvasCustomizer.jsx:115  Zone Update [zone-337-4] 
CanvasCustomizer.jsx:116 "x": 276, "y": 532, "angle": 0
CanvasCustomizer.jsx:117 --------------------------



product id :338
--------------------------
CanvasCustomizer.jsx:115  Zone Update [zone-338-1] 
CanvasCustomizer.jsx:116 "x": 372, "y": 403, "angle": 0
CanvasCustomizer.jsx:117 --------------------------
CanvasCustomizer.jsx:115  Zone Update [zone-338-2] 
CanvasCustomizer.jsx:116 "x": 741, "y": 475, "angle": 64
CanvasCustomizer.jsx:117 --------------------------
CanvasCustomizer.jsx:115  Zone Update [zone-338-3] 
CanvasCustomizer.jsx:116 "x": 418, "y": 652, "angle": 0
CanvasCustomizer.jsx:117 --------------------------
CanvasCustomizer.jsx:115  Zone Update [zone-338-4] 
CanvasCustomizer.jsx:116 "x": 416, "y": 696, "angle": 0
CanvasCustomizer.jsx:117 --------------------------
CanvasCustomizer.jsx:115  Zone Update [zone-338-5] 
CanvasCustomizer.jsx:116 "x": 414, "y": 732, "angle": 0
CanvasCustomizer.jsx:117 --------------------------



product id :339
--------------------------
CanvasCustomizer.jsx:115  Zone Update [zone-339-1] 
CanvasCustomizer.jsx:116 "x": 368, "y": 389, "angle": 0
CanvasCustomizer.jsx:117 --------------------------
CanvasCustomizer.jsx:115  Zone Update [zone-339-2] 
CanvasCustomizer.jsx:116 "x": 775, "y": 469, "angle": 66
CanvasCustomizer.jsx:117 --------------------------
CanvasCustomizer.jsx:115  Zone Update [zone-339-3] 
CanvasCustomizer.jsx:116 "x": 464, "y": 634, "angle": 0
CanvasCustomizer.jsx:117 --------------------------
CanvasCustomizer.jsx:115  Zone Update [zone-339-4] 
CanvasCustomizer.jsx:116 "x": 462, "y": 678, "angle": 0
CanvasCustomizer.jsx:117 --------------------------
CanvasCustomizer.jsx:115  Zone Update [zone-339-5] 
CanvasCustomizer.jsx:116 "x": 460, "y": 724, "angle": 0


product id :340
--------------------------
CanvasCustomizer.jsx:115  Zone Update [zone-340-1] 
CanvasCustomizer.jsx:116 "x": 364, "y": 401, "angle": 0
CanvasCustomizer.jsx:117 --------------------------
CanvasCustomizer.jsx:115  Zone Update [zone-340-2] 
CanvasCustomizer.jsx:116 "x": 784, "y": 474, "angle": 67
CanvasCustomizer.jsx:117 --------------------------
CanvasCustomizer.jsx:115  Zone Update [zone-340-3] 
CanvasCustomizer.jsx:116 "x": 404, "y": 622, "angle": 0
CanvasCustomizer.jsx:117 --------------------------
CanvasCustomizer.jsx:115  Zone Update [zone-340-4] 
CanvasCustomizer.jsx:116 "x": 404, "y": 668, "angle": 0
CanvasCustomizer.jsx:117 --------------------------
CanvasCustomizer.jsx:115  Zone Update [zone-340-5] 
CanvasCustomizer.jsx:116 "x": 400, "y": 714, "angle": 0


product id :341
--------------------------
CanvasCustomizer.jsx:115  Zone Update [zone-341-1] 
CanvasCustomizer.jsx:116 "x": 474, "y": 111, "angle": 0
CanvasCustomizer.jsx:117 --------------------------
CanvasCustomizer.jsx:115  Zone Update [zone-341-2] 
CanvasCustomizer.jsx:116 "x": 500, "y": 300, "angle": 0
CanvasCustomizer.jsx:117 --------------------------
CanvasCustomizer.jsx:115  Zone Update [zone-341-3] 
CanvasCustomizer.jsx:116 "x": 500, "y": 400, "angle": 0
CanvasCustomizer.jsx:117 --------------------------
CanvasCustomizer.jsx:115  Zone Update [zone-341-4] 
CanvasCustomizer.jsx:116 "x": 494, "y": 498, "angle": 0
CanvasCustomizer.jsx:117 --------------------------
CanvasCustomizer.jsx:115  Zone Update [zone-341-5] 
CanvasCustomizer.jsx:116 "x": 488, "y": 602, "angle": 0


product id :342
--------------------------
CanvasCustomizer.jsx:115  Zone Update [zone-342-1] 
CanvasCustomizer.jsx:116 "x": 512, "y": 131, "angle": 0
CanvasCustomizer.jsx:117 --------------------------
CanvasCustomizer.jsx:115  Zone Update [zone-342-1] 
CanvasCustomizer.jsx:116 "x": 494, "y": 127, "angle": 0
CanvasCustomizer.jsx:117 --------------------------
CanvasCustomizer.jsx:115  Zone Update [zone-342-2] 
CanvasCustomizer.jsx:116 "x": 498, "y": 300, "angle": 0
CanvasCustomizer.jsx:117 --------------------------
CanvasCustomizer.jsx:115  Zone Update [zone-342-3] 
CanvasCustomizer.jsx:116 "x": 498, "y": 396, "angle": 0
CanvasCustomizer.jsx:117 --------------------------
CanvasCustomizer.jsx:115  Zone Update [zone-342-4] 
CanvasCustomizer.jsx:116 "x": 498, "y": 500, "angle": 0
CanvasCustomizer.jsx:117 --------------------------
CanvasCustomizer.jsx:115  Zone Update [zone-342-5] 
CanvasCustomizer.jsx:116 "x": 498, "y": 600, "angle": 0


product id :343
--------------------------
CanvasCustomizer.jsx:115  Zone Update [zone-343-1] 
CanvasCustomizer.jsx:116 "x": 475, "y": 128, "angle": 0
CanvasCustomizer.jsx:117 --------------------------
CanvasCustomizer.jsx:115  Zone Update [zone-343-2] 
CanvasCustomizer.jsx:116 "x": 498, "y": 306, "angle": 0
CanvasCustomizer.jsx:117 --------------------------
CanvasCustomizer.jsx:115  Zone Update [zone-343-3] 
CanvasCustomizer.jsx:116 "x": 492, "y": 394, "angle": 0
CanvasCustomizer.jsx:117 --------------------------
CanvasCustomizer.jsx:115  Zone Update [zone-343-4] 
CanvasCustomizer.jsx:116 "x": 500, "y": 496, "angle": 0
CanvasCustomizer.jsx:117 --------------------------
CanvasCustomizer.jsx:115  Zone Update [zone-343-5] 
CanvasCustomizer.jsx:116 "x": 500, "y": 596, "angle": 0


product id :344
--------------------------
CanvasCustomizer.jsx:115  Zone Update [zone-344-1] 
CanvasCustomizer.jsx:116 "x": 476, "y": 135, "angle": 0
CanvasCustomizer.jsx:117 --------------------------
CanvasCustomizer.jsx:115  Zone Update [zone-344-2] 
CanvasCustomizer.jsx:116 "x": 498, "y": 300, "angle": 0
CanvasCustomizer.jsx:117 --------------------------
CanvasCustomizer.jsx:115  Zone Update [zone-344-3] 
CanvasCustomizer.jsx:116 "x": 498, "y": 394, "angle": 0
CanvasCustomizer.jsx:117 --------------------------
CanvasCustomizer.jsx:115  Zone Update [zone-344-4] 
CanvasCustomizer.jsx:116 "x": 500, "y": 488, "angle": 0
CanvasCustomizer.jsx:117 --------------------------
CanvasCustomizer.jsx:115  Zone Update [zone-344-5] 
CanvasCustomizer.jsx:116 "x": 500, "y": 594, "angle": 0


product id :345
--------------------------
CanvasCustomizer.jsx:115  Zone Update [zone-345-1] 
CanvasCustomizer.jsx:116 "x": 489, "y": 103, "angle": 0
CanvasCustomizer.jsx:117 --------------------------
CanvasCustomizer.jsx:115  Zone Update [zone-345-2] 
CanvasCustomizer.jsx:116 "x": 500, "y": 300, "angle": 0
CanvasCustomizer.jsx:117 --------------------------
CanvasCustomizer.jsx:115  Zone Update [zone-345-3] 
CanvasCustomizer.jsx:116 "x": 500, "y": 388, "angle": 0
CanvasCustomizer.jsx:117 --------------------------
CanvasCustomizer.jsx:115  Zone Update [zone-345-4] 
CanvasCustomizer.jsx:116 "x": 494, "y": 454, "angle": 0
CanvasCustomizer.jsx:117 --------------------------
CanvasCustomizer.jsx:115  Zone Update [zone-345-5] 
CanvasCustomizer.jsx:116 "x": 492, "y": 566, "angle": 0


product id :346
--------------------------
CanvasCustomizer.jsx:115  Zone Update [zone-346-1] 
CanvasCustomizer.jsx:116 "x": 489, "y": 125, "angle": 0
CanvasCustomizer.jsx:117 --------------------------
CanvasCustomizer.jsx:115  Zone Update [zone-346-2] 
CanvasCustomizer.jsx:116 "x": 500, "y": 300, "angle": 0
CanvasCustomizer.jsx:117 --------------------------
CanvasCustomizer.jsx:115  Zone Update [zone-346-3] 
CanvasCustomizer.jsx:116 "x": 502, "y": 400, "angle": 0
CanvasCustomizer.jsx:117 --------------------------
CanvasCustomizer.jsx:115  Zone Update [zone-346-4] 
CanvasCustomizer.jsx:116 "x": 500, "y": 504, "angle": 0
CanvasCustomizer.jsx:117 --------------------------
CanvasCustomizer.jsx:115  Zone Update [zone-346-5] 
CanvasCustomizer.jsx:116 "x": 494, "y": 600, "angle": 0
CanvasCustomizer.jsx:117 --------------------------


product id :347
--------------------------
CanvasCustomizer.jsx:115  Zone Update [zone-347-1] 
CanvasCustomizer.jsx:116 "x": 494, "y": 127, "angle": 0
CanvasCustomizer.jsx:117 --------------------------
CanvasCustomizer.jsx:115  Zone Update [zone-347-2] 
CanvasCustomizer.jsx:116 "x": 500, "y": 294, "angle": 0
CanvasCustomizer.jsx:117 --------------------------
CanvasCustomizer.jsx:115  Zone Update [zone-347-3] 
CanvasCustomizer.jsx:116 "x": 500, "y": 390, "angle": 0
CanvasCustomizer.jsx:117 --------------------------
CanvasCustomizer.jsx:115  Zone Update [zone-347-4] 
CanvasCustomizer.jsx:116 "x": 500, "y": 480, "angle": 0
CanvasCustomizer.jsx:117 --------------------------
CanvasCustomizer.jsx:115  Zone Update [zone-347-5] 
CanvasCustomizer.jsx:116 "x": 502, "y": 574, "angle": 0
CanvasCustomizer.jsx:117 --------------------------



product id :348
--------------------------
CanvasCustomizer.jsx:115  Zone Update [zone-348-1] 
CanvasCustomizer.jsx:116 "x": 472, "y": 107, "angle": 0
CanvasCustomizer.jsx:117 --------------------------
CanvasCustomizer.jsx:115  Zone Update [zone-348-2] 
CanvasCustomizer.jsx:116 "x": 500, "y": 296, "angle": 0
CanvasCustomizer.jsx:117 --------------------------
CanvasCustomizer.jsx:115  Zone Update [zone-348-3] 
CanvasCustomizer.jsx:116 "x": 500, "y": 392, "angle": 0
CanvasCustomizer.jsx:117 --------------------------
CanvasCustomizer.jsx:115  Zone Update [zone-348-4] 
CanvasCustomizer.jsx:116 "x": 498, "y": 498, "angle": 0
CanvasCustomizer.jsx:117 --------------------------
CanvasCustomizer.jsx:115  Zone Update [zone-348-5] 
CanvasCustomizer.jsx:116 "x": 500, "y": 594, "angle": 0
CanvasCustomizer.jsx:117 --------------------------


product id :349
--------------------------
CanvasCustomizer.jsx:115  Zone Update [zone-349-1] 
CanvasCustomizer.jsx:116 "x": 491, "y": 148, "angle": 0
CanvasCustomizer.jsx:117 --------------------------
CanvasCustomizer.jsx:115  Zone Update [zone-349-4] 
CanvasCustomizer.jsx:116 "x": 382, "y": 354, "angle": 0
CanvasCustomizer.jsx:117 --------------------------
CanvasCustomizer.jsx:115  Zone Update [zone-349-2] 
CanvasCustomizer.jsx:116 "x": 462, "y": 312, "angle": 0
CanvasCustomizer.jsx:117 --------------------------
CanvasCustomizer.jsx:115  Zone Update [zone-349-3] 
CanvasCustomizer.jsx:116 "x": 457, "y": 403, "angle": 0
CanvasCustomizer.jsx:117 --------------------------
CanvasCustomizer.jsx:115  Zone Update [zone-349-5] 
CanvasCustomizer.jsx:116 "x": 450, "y": 480, "angle": 0


product id :350


product id :351
--------------------------
CanvasCustomizer.jsx:115  Zone Update [text-zone-1] 
CanvasCustomizer.jsx:116 "x": 496, "y": 538, "angle": 0
CanvasCustomizer.jsx:117 --------------------------
CanvasCustomizer.jsx:115  Zone Update [extra-1] 
CanvasCustomizer.jsx:116 "x": 502, "y": 378, "angle": 0
CanvasCustomizer.jsx:117 --------------------------
CanvasCustomizer.jsx:115  Zone Update [name-1] 
CanvasCustomizer.jsx:116 "x": 522, "y": 152, "angle": 0

product id :352
--------------------------
CanvasCustomizer.jsx:115  Zone Update [name-1] 
CanvasCustomizer.jsx:116 "x": 478, "y": 668, "angle": 277
CanvasCustomizer.jsx:117 --------------------------
CanvasCustomizer.jsx:115  Zone Update [extra-1] 
CanvasCustomizer.jsx:116 "x": 500, "y": 348, "angle": 0
CanvasCustomizer.jsx:117 --------------------------
CanvasCustomizer.jsx:115  Zone Update [extra-2] 
CanvasCustomizer.jsx:116 "x": 500, "y": 442, "angle": 0
CanvasCustomizer.jsx:117 --------------------------

product id :353
--------------------------
CanvasCustomizer.jsx:115  Zone Update [name-1] 
CanvasCustomizer.jsx:116 "x": 468, "y": 666, "angle": 276
CanvasCustomizer.jsx:117 --------------------------
CanvasCustomizer.jsx:115  Zone Update [extra-1] 
CanvasCustomizer.jsx:116 "x": 500, "y": 340, "angle": 0
CanvasCustomizer.jsx:117 --------------------------
CanvasCustomizer.jsx:115  Zone Update [extra-2] 
CanvasCustomizer.jsx:116 "x": 500, "y": 412, "angle": 0
CanvasCustomizer.jsx:117 --------------------------


product id :354
--------------------------
CanvasCustomizer.jsx:115  Zone Update [name-1] 
CanvasCustomizer.jsx:116 "x": 473, "y": 656, "angle": 275
CanvasCustomizer.jsx:117 --------------------------
CanvasCustomizer.jsx:115  Zone Update [extra-1] 
CanvasCustomizer.jsx:116 "x": 506, "y": 344, "angle": 0
CanvasCustomizer.jsx:117 --------------------------
CanvasCustomizer.jsx:115  Zone Update [extra-2] 
CanvasCustomizer.jsx:116 "x": 502, "y": 444, "angle": 0
CanvasCustomizer.jsx:117 --------------------------

product id :355
--------------------------
CanvasCustomizer.jsx:115  Zone Update [name-1] 
CanvasCustomizer.jsx:116 "x": 470, "y": 674, "angle": 270
CanvasCustomizer.jsx:117 --------------------------
CanvasCustomizer.jsx:115  Zone Update [extra-1] 
CanvasCustomizer.jsx:116 "x": 500, "y": 346, "angle": 0
CanvasCustomizer.jsx:117 --------------------------
CanvasCustomizer.jsx:115  Zone Update [extra-2] 
CanvasCustomizer.jsx:116 "x": 500, "y": 446, "angle": 0

product id :356
--------------------------
CanvasCustomizer.jsx:115  Zone Update [name-1] 
CanvasCustomizer.jsx:116 "x": 484, "y": 656, "angle": 272
CanvasCustomizer.jsx:117 --------------------------
CanvasCustomizer.jsx:115  Zone Update [extra-1] 
CanvasCustomizer.jsx:116 "x": 502, "y": 344, "angle": 0
CanvasCustomizer.jsx:117 --------------------------
CanvasCustomizer.jsx:115  Zone Update [extra-2] 
CanvasCustomizer.jsx:116 "x": 500, "y": 444, "angle": 0
CanvasCustomizer.jsx:117 --------------------------


product id :357
--------------------------
CanvasCustomizer.jsx:115  Zone Update [name-1] 
CanvasCustomizer.jsx:116 "x": 472, "y": 676, "angle": 274
CanvasCustomizer.jsx:117 --------------------------
CanvasCustomizer.jsx:115  Zone Update [extra-1] 
CanvasCustomizer.jsx:116 "x": 500, "y": 364, "angle": 0
CanvasCustomizer.jsx:117 --------------------------
CanvasCustomizer.jsx:115  Zone Update [extra-2] 
CanvasCustomizer.jsx:116 "x": 500, "y": 446, "angle": 0
CanvasCustomizer.jsx:117 --------------------------


product id :358
 Customizer Engine Ready 
CanvasCustomizer.jsx:115  Zone Update [name-1] 
CanvasCustomizer.jsx:116 "x": 674, "y": 514, "angle": 0
CanvasCustomizer.jsx:117 --------------------------
CanvasCustomizer.jsx:115  Zone Update [extra-1] 
CanvasCustomizer.jsx:116 "x": 526, "y": 142, "angle": 0
CanvasCustomizer.jsx:117 --------------------------
CanvasCustomizer.jsx:115  Zone Update [extra-2] 
CanvasCustomizer.jsx:116 "x": 536, "y": 216, "angle": 0
CanvasCustomizer.jsx:117 --------------------------

product id :359
--------------------------
CanvasCustomizer.jsx:115  Zone Update [name-1] 
CanvasCustomizer.jsx:116 "x": 438, "y": 700, "angle": 0
CanvasCustomizer.jsx:117 --------------------------
CanvasCustomizer.jsx:115  Zone Update [extra-1] 
CanvasCustomizer.jsx:116 "x": 154, "y": 643, "angle": 0
CanvasCustomizer.jsx:117 --------------------------
CanvasCustomizer.jsx:115  Zone Update [extra-2] 
CanvasCustomizer.jsx:116 "x": 436, "y": 354, "angle": 0
CanvasCustomizer.jsx:117 --------------------------

product id :360
--------------------------
CanvasCustomizer.jsx:115  Zone Update [name-1] 
CanvasCustomizer.jsx:116 "x": 470, "y": 860, "angle": 0
CanvasCustomizer.jsx:117 --------------------------
CanvasCustomizer.jsx:115  Zone Update [extra-1] 
CanvasCustomizer.jsx:116 "x": 522, "y": 154, "angle": 0
CanvasCustomizer.jsx:117 --------------------------
CanvasCustomizer.jsx:115  Zone Update [extra-2] 
CanvasCustomizer.jsx:116 "x": 266, "y": 650, "angle": 0
CanvasCustomizer.jsx:117 --------------------------

product id :361
 Zone Update [name-1] 
CanvasCustomizer.jsx:116 "x": 440, "y": 602, "angle": 0
CanvasCustomizer.jsx:117 --------------------------
CanvasCustomizer.jsx:115  Zone Update [extra-1] 
CanvasCustomizer.jsx:116 "x": 506, "y": 154, "angle": 0
CanvasCustomizer.jsx:117 --------------------------
CanvasCustomizer.jsx:115  Zone Update [extra-2] 
CanvasCustomizer.jsx:116 "x": 514, "y": 250, "angle": 0
CanvasCustomizer.jsx:117 --------------------------

product id :362
--------------------------
CanvasCustomizer.jsx:115  Zone Update [name-1] 
CanvasCustomizer.jsx:116 "x": 650, "y": 780, "angle": 348
CanvasCustomizer.jsx:117 --------------------------
CanvasCustomizer.jsx:115  Zone Update [extra-1] 
CanvasCustomizer.jsx:116 "x": 492, "y": 94, "angle": 0
CanvasCustomizer.jsx:117 --------------------------
CanvasCustomizer.jsx:115  Zone Update [extra-2] 
CanvasCustomizer.jsx:116 "x": 484, "y": 146, "angle": 0


product id :363
--------------------------
CanvasCustomizer.jsx:115  Zone Update [name-1] 
CanvasCustomizer.jsx:116 "x": 556, "y": 856, "angle": 352
CanvasCustomizer.jsx:117 --------------------------
CanvasCustomizer.jsx:115  Zone Update [extra-1] 
CanvasCustomizer.jsx:116 "x": 226, "y": 624, "angle": 268
CanvasCustomizer.jsx:117 --------------------------
CanvasCustomizer.jsx:115  Zone Update [extra-2] 
CanvasCustomizer.jsx:116 "x": 498, "y": 148, "angle": 0
CanvasCustomizer.jsx:117 --------------------------


product id :364
--------------------------
CanvasCustomizer.jsx:115  Zone Update [name-1] 
CanvasCustomizer.jsx:116 "x": 534, "y": 872, "angle": 0
CanvasCustomizer.jsx:117 --------------------------
CanvasCustomizer.jsx:115  Zone Update [extra-1] 
CanvasCustomizer.jsx:116 "x": 196, "y": 620, "angle": 268
CanvasCustomizer.jsx:117 --------------------------
CanvasCustomizer.jsx:115  Zone Update [extra-2] 
CanvasCustomizer.jsx:116 "x": 500, "y": 148, "angle": 0
CanvasCustomizer.jsx:117 --------------------------


product id :365
--------------------------
CanvasCustomizer.jsx:115  Zone Update [name-1] 
CanvasCustomizer.jsx:116 "x": 534, "y": 872, "angle": 0
CanvasCustomizer.jsx:117 --------------------------
CanvasCustomizer.jsx:115  Zone Update [extra-1] 
CanvasCustomizer.jsx:116 "x": 196, "y": 620, "angle": 268
CanvasCustomizer.jsx:117 --------------------------
CanvasCustomizer.jsx:115  Zone Update [extra-2] 
CanvasCustomizer.jsx:116 "x": 500, "y": 148, "angle": 0
CanvasCustomizer.jsx:117 --------------------------

product id :366
--------------------------
CanvasCustomizer.jsx:115  Zone Update [name-1] 
CanvasCustomizer.jsx:116 "x": 596, "y": 840, "angle": 0
CanvasCustomizer.jsx:117 --------------------------
CanvasCustomizer.jsx:115  Zone Update [extra-1] 
CanvasCustomizer.jsx:116 "x": 275, "y": 697, "angle": 261
CanvasCustomizer.jsx:117 --------------------------
CanvasCustomizer.jsx:115  Zone Update [extra-2] 
CanvasCustomizer.jsx:116 "x": 552, "y": 220, "angle": 341

product id :367
--------------------------
CanvasCustomizer.jsx:115  Zone Update [name-1] 
CanvasCustomizer.jsx:116 "x": 683, "y": 721, "angle": 346
CanvasCustomizer.jsx:117 --------------------------
CanvasCustomizer.jsx:115  Zone Update [extra-1] 
CanvasCustomizer.jsx:116 "x": 466, "y": 138, "angle": 0
CanvasCustomizer.jsx:117 --------------------------
CanvasCustomizer.jsx:115  Zone Update [extra-2] 
CanvasCustomizer.jsx:116 "x": 407, "y": 648, "angle": 354
CanvasCustomizer.jsx:117 --------------------------


product id :368
Zone Update [name-1] 
CanvasCustomizer.jsx:116 "x": 670, "y": 652, "angle": 0
CanvasCustomizer.jsx:117 --------------------------
CanvasCustomizer.jsx:115  Zone Update [extra-1] 
CanvasCustomizer.jsx:116 "x": 228, "y": 634, "angle": 0
CanvasCustomizer.jsx:117 --------------------------
CanvasCustomizer.jsx:115  Zone Update [extra-2] 
CanvasCustomizer.jsx:116 "x": 672, "y": 500, "angle": 0
CanvasCustomizer.jsx:117 --------------------------


product id :369
--------------------------
CanvasCustomizer.jsx:115  Zone Update [name-1] 
CanvasCustomizer.jsx:116 "x": 604, "y": 788, "angle": 0
CanvasCustomizer.jsx:117 --------------------------
CanvasCustomizer.jsx:115  Zone Update [extra-1] 
CanvasCustomizer.jsx:116 "x": 236, "y": 392, "angle": 266
CanvasCustomizer.jsx:117 --------------------------
CanvasCustomizer.jsx:115  Zone Update [extra-2] 
CanvasCustomizer.jsx:116 "x": 574, "y": 50, "angle": 0
CanvasCustomizer.jsx:117 --------------------------

product id :370
--------------------------
CanvasCustomizer.jsx:115  Zone Update [name-1] 
CanvasCustomizer.jsx:116 "x": 539, "y": 664, "angle": 349
CanvasCustomizer.jsx:117 --------------------------
CanvasCustomizer.jsx:115  Zone Update [extra-1] 
CanvasCustomizer.jsx:116 "x": 833, "y": 548, "angle": 351
CanvasCustomizer.jsx:117 --------------------------
CanvasCustomizer.jsx:115  Zone Update [extra-2] 
CanvasCustomizer.jsx:116 "x": 492, "y": 154, "angle": 0
CanvasCustomizer.jsx:117 --------------------------
"""

def parse_logs():
    data = {}
    current_db_id = None
    current_zone = None
    
    lines = RAW_LOGS.strip().split('\n')
    for line in lines:
        line = line.strip()
        if not line:
            continue
            
        # Match product id
        prod_match = re.search(r'(?i)product\s*id\s*:\s*(\d+)', line)
        if prod_match:
            current_db_id = int(prod_match.group(1))
            if current_db_id not in data:
                data[current_db_id] = {}
            current_zone = None
            continue
            
        # Match Zone Update
        zone_match = re.search(r'(?i)Zone Update\s+\[(.*?)\]', line)
        if zone_match:
            current_zone = zone_match.group(1).strip()
            continue
            
        # Match coordinates
        coord_match = re.search(r'"x"\s*:\s*(-?\d+),\s*"y"\s*:\s*(-?\d+),\s*"angle"\s*:\s*(-?\d+)', line)
        if coord_match and current_db_id and current_zone:
            x = int(coord_match.group(1))
            y = int(coord_match.group(2))
            angle = int(coord_match.group(3))
            
            # This automatically keeps the latest values in case of duplicates
            data[current_db_id][current_zone] = {
                'x': x,
                'y': y,
                'angle': angle
            }
            
    return data

def main():
    parsed = parse_logs()
    print(f"[INFO] Parsed logs for {len(parsed)} products.")
    
    # Load customization.json
    if not os.path.exists(FRONTEND_JSON_PATH):
        print(f"[ERROR] customization.json not found at {FRONTEND_JSON_PATH}")
        sys.exit(1)
        
    with open(FRONTEND_JSON_PATH, 'r', encoding='utf-8') as f:
        customization_data = json.load(f)
        
    print(f"[INFO] Loaded customization.json with {len(customization_data)} items.")
    
    # Map DB ID -> Slug, and create updates map
    slug_updates = {}
    for db_id, zones_coords in parsed.items():
        if not zones_coords:
            print(f"[INFO] Skipping Product ID {db_id} - no coordinates found.")
            continue
            
        try:
            product = Product.objects.get(id=db_id)
            slug = product.slug
            slug_updates[slug] = zones_coords
            print(f"[INFO] Mapped DB ID {db_id} to slug: '{slug}' ({product.name})")
        except Product.DoesNotExist:
            print(f"[WARNING] Product with ID {db_id} not found in Django Database!")
            
    # Apply updates to customization.json
    updated_products_count = 0
    for item in customization_data:
        slug = item.get('slug')
        if slug in slug_updates:
            print(f"\nUpdating zones for slug: '{slug}':")
            coords_map = slug_updates[slug]
            
            zones = item.get('zones', [])
            updated_any = False
            for zone in zones:
                z_id = zone.get('id')
                if z_id in coords_map:
                    new_coords = coords_map[z_id]
                    print(f"  Zone '{z_id}': x={zone.get('x')} -> {new_coords['x']}, y={zone.get('y')} -> {new_coords['y']}, angle={zone.get('angle')} -> {new_coords['angle']}")
                    zone['x'] = new_coords['x']
                    zone['y'] = new_coords['y']
                    zone['angle'] = new_coords['angle']
                    updated_any = True
                    
            if updated_any:
                updated_products_count += 1
                
    # Save back customization.json
    with open(FRONTEND_JSON_PATH, 'w', encoding='utf-8') as f:
        json.dump(customization_data, f, indent=2)
        
    print(f"\n[SUCCESS] Wrote updates to customization.json for {updated_products_count} products.")
    
    # Run sync_customization.py to update SQLite database
    print("\n" + "="*50)
    print("RUNNING SYNC TO SQLITE DATABASE")
    print("="*50)
    
    sync_script_path = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 'sync_customization.py')
    if os.path.exists(sync_script_path):
        import subprocess
        try:
            res = subprocess.run([sys.executable, sync_script_path], capture_output=True, text=True, check=True)
            print(res.stdout)
            print("[SUCCESS] SQLite database sync completed successfully!")
        except subprocess.CalledProcessError as e:
            print(f"[ERROR] Database sync failed: {e}")
            print(e.stderr)
            sys.exit(1)
    else:
        print(f"[ERROR] sync_customization.py not found at {sync_script_path}")
        sys.exit(1)

if __name__ == '__main__':
    main()
