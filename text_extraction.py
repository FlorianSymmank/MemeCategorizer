import json
import os

import pytesseract
from PIL import Image

import config
from persistance import load_data, save_data

# Defining paths to tesseract.exe
pytesseract.pytesseract.tesseract_cmd = config.tesseract_cmd


def main():

    # find all non text extracted images
    data_files = os.listdir(config.processed_meme_dir)
    files_text_missing = [load_data(os.path.splitext(file)[
                                    0]) for file in data_files if "text" not in load_data(os.path.splitext(file)[0])]

    # could be a lengthy operation some feedback
    f_count = 0
    f_len = len(files_text_missing)
    info_increment = 0.1
    next_info = info_increment

    for data in files_text_missing:
        file = data["id"] + ".tiff"
        path = os.path.join(config.processed_meme_dir, file)
        img = Image.open(path)
        text = pytesseract.image_to_string(img)

        # clean text
        text = text.rstrip()
        text = text.lstrip()
        text = " ".join([s for s in text.splitlines() if s])
        data["text"] = text
        save_data(data)

        # feedback
        if (f_count/f_len >= next_info):
            print(f"{(next_info * 100):.0f} %")
            next_info += info_increment

        f_count = f_count + 1

    print("Done")


if __name__ == "__main__":
    main()
