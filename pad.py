from PIL import Image, ImageOps
import os
from pathlib import Path
from typing import List
import config
from persistance import load_data, save_data

def main():

    data_files = os.listdir(config.processed_meme_dir)
    padded = os.listdir(config.padded_meme_dir)

    missing = [load_data(os.path.splitext(file)[
                                    0]) for file in data_files if "mean_color" in load_data(os.path.splitext(file)[0]) and Path('/root/dir/sub/file.ext').stem not in padded]

    f_count = 0
    f_len = len(missing)
    info_increment = 0.1
    next_info = info_increment

    for data in missing:
        file = data["id"] + ".tiff"
        path = os.path.join(config.processed_meme_dir, file)
        tiff_padded_mean = os.path.join(config.padded_meme_dir, f"mean_{file}")
        tiff_padded = os.path.join(config.padded_meme_dir, f"median_{file}")

        size = (300, 300)
        with Image.open(path) as im:
            ImageOps.pad(im, size, color=RGB_to_HEX(data["mean_color"])).save(tiff_padded_mean)
            # median colors looks better
            ImageOps.pad(im, size, color=RGB_to_HEX(data["median_color"])).save(tiff_padded)
                                                                              
        # feedback
        if (f_count/f_len >= next_info):
            print(f"{(next_info * 100):.0f} %")
            next_info += info_increment

        f_count = f_count + 1

    print("Done")

def RGB_to_HEX(rgb_vals: List[int]) -> str:
        
        # make sure its ints
        rgb_vals = [int(val) for val in rgb_vals] 

        r, g, b = rgb_vals
        return f'#{r << 16 | g << 8 | b:06x}'

if __name__ == "__main__":
    main()