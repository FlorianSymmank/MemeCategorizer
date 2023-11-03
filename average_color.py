from PIL import Image, ImageStat
import json
import os

import config
from persistance import load_data, save_data

def main():

    data_files = os.listdir(config.processed_meme_dir)
    files_avg_color_missing = [load_data(os.path.splitext(file)[
                                    0]) for file in data_files if "mean_color" not in load_data(os.path.splitext(file)[0])]

    f_count = 0
    f_len = len(files_avg_color_missing)
    info_increment = 0.1
    next_info = info_increment

    for data in files_avg_color_missing:
        file = data["id"] + ".tiff"
        path = os.path.join(config.processed_meme_dir, file)

        with Image.open(path) as img:
            if img.mode != "RGB":
                img = img.convert("RGB")

            stat = ImageStat.Stat(img)
            data["mean_color"] = stat.mean[0:3]
            data["median_color"] = stat.median[0:3]
            save_data(data)

        # feedback
        if (f_count/f_len >= next_info):
            print(f"{(next_info * 100):.0f} %")
            next_info += info_increment

        f_count = f_count + 1

    print("Done")


if __name__ == "__main__":
    main()
