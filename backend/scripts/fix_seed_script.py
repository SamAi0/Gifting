import re

filepath = 'seed_products.py'
with open(filepath, 'r') as f:
    content = f.read()

# Fix the broken lines like 'mug.png",' or 'sr_125_pen_keychain_cardholder.png",'
# The current broken line looks like: '            mug.png",'
# We want: '            "image": "static/products/mug.png",'

fixed_content = re.sub(r'(\s+)([a-zA-Z0-9_]+\.png",)', r'\1"image": "static/products/\2', content)

with open(filepath, 'w') as f:
    f.write(fixed_content)

print("Fixed seed_products.py")
