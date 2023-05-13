import os
import re

from PIL import Image

preprocessed_dir = "F:\VisualStudioProjekte\MemeCategorizer\preprocessed"
meme_dir = r"F:\Wichtige Dokumente\Box Sync\Memes"

# find all non preprocessed images
files_processed = os.listdir(preprocessed_dir)
files = [f for f in os.listdir(
    meme_dir) if re.search(r'.*\.(jpg|webp|png)', f) and 
    os.path.splitext(f)[0] + ".tiff" not in files_processed]

# could be a lengthy operation some feedback
f_count = 0
f_len = len(files)
info_increment = 0.1
next_info = info_increment

for file in files:

    # new filename
    filename, file_extension = os.path.splitext(file)
    tiff = os.path.join(preprocessed_dir, filename) + ".tiff"

    # convert
    path = os.path.join(meme_dir, file)
    im = Image.open(path)
    im.save(tiff, 'TIFF')

    # feedback
    if (f_count/f_len >= next_info):
        print(f"{(next_info * 100):.0f} %")
        next_info += info_increment

    f_count = f_count + 1

print("Done")
