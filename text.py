import json
import os
import re

import pytesseract
from PIL import Image

# Defining paths to tesseract.exe
pytesseract.pytesseract.tesseract_cmd = 'C:\\Program Files\\Tesseract-OCR\\tesseract.exe'

meme_dir = r"F:\VisualStudioProjekte\MemeCategorizer\preprocessed"
data_dir = f"F:\VisualStudioProjekte\MemeCategorizer\data"


def load_data(id):
    file_path = os.path.join(data_dir, id) + ".json"
    if os.path.isfile(file_path):
        f = open(file_path)
        return json.load(f)
    else:
        return {"id": id}


def save_data(data):
    path = f"{os.path.join(data_dir, data['id'])}.json"
    with open(path, 'w') as f:
        json.dump(data, f, indent=4, sort_keys=True)


def main():

    # find all non text extracted images
    data_files = os.listdir(meme_dir)
    files_text_missing = [load_data(os.path.splitext(file)[
                                    0]) for file in data_files if "text" not in load_data(os.path.splitext(file)[0])]

    # could be a lengthy operation some feedback
    f_count = 0
    f_len = len(files_text_missing)
    info_increment = 0.1
    next_info = info_increment

    for data in files_text_missing:
        file = data["id"] + ".tiff"
        path = os.path.join(meme_dir, file)
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
