import re
text = '''
products/106
set placeholder name zones 1-Your name,2-Pen text
 Zone Update [zone-106-1] 
CanvasCustomizer.jsx:116 "x": 600, "y": 306, "angle": 0
CanvasCustomizer.jsx:117 --------------------------
CanvasCustomizer.jsx:115  Zone Update [zone-106-2] 
CanvasCustomizer.jsx:116 "x": 813, "y": 572, "angle": 89
'''
zones = re.findall(r'(?i)zone update\s*\[([^\]]+)\][\s\S]*?CanvasCustomizer\.jsx:116\s*"x"\s*:\s*(-?\d+),\s*"y"\s*:\s*(-?\d+),\s*"angle"\s*:\s*(-?\d+)', text)
print(zones)
