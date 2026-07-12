import os
from PIL import Image

static_dir = os.path.abspath('static/products')
files = os.listdir(static_dir)
corrupt = []
for f in files:
    if os.path.isfile(os.path.join(static_dir, f)):
        try:
            with Image.open(os.path.join(static_dir, f)) as img:
                img.verify()
        except Exception as e:
            corrupt.append(f)

if corrupt:
    print('Corrupt files:', corrupt)
else:
    print('No corrupt files found.')
