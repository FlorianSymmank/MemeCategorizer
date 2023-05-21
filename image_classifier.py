import json
import os

import numpy as np
from tensorflow.keras.applications.efficientnet import (EfficientNetB7,
                                                        decode_predictions,
                                                        preprocess_input)
from tensorflow.keras.preprocessing import image

import config
from persistance import load_data, save_data

model = EfficientNetB7(weights='imagenet')


def preprocess_image(image_path):
    img = image.load_img(image_path, target_size=(600, 600))
    x = image.img_to_array(img)
    x = np.expand_dims(x, axis=0)
    x = preprocess_input(x)
    return x


def predict_images(image_paths):
    batch = np.vstack([preprocess_image(p) for p in image_paths])
    predictions = model.predict(batch)
    decoded_preds = decode_predictions(predictions, top=5)
    return decoded_preds


def subbatches(arr, batch_size=10):
    num_batches = np.ceil(len(arr) / batch_size).astype(int)
    return np.array_split(arr, num_batches)


def main():

    # find all non tagged images
    data_files = os.listdir(config.processed_meme_dir)
    files_tags_missing = [load_data(os.path.splitext(file)[
                                    0]) for file in data_files if "tags" not in load_data(os.path.splitext(file)[0])]

    if len(files_tags_missing) == 0:
        print("Done")
        return

    batches = subbatches(files_tags_missing)

    # could be a lengthy operation some feedback
    f_count = 0
    f_len = len(batches)
    info_increment = 0.1
    next_info = info_increment

    for subbatch in batches:
        image_paths = [os.path.join(config.processed_meme_dir, data["id"] + ".tiff")
                       for data in subbatch]

        preds = predict_images(image_paths)
        for i, preds in enumerate(preds):
            data = subbatch[i]
            data["tags"] = [prediction[1] for prediction in preds]
            save_data(data)

        # feedback
        if (f_count/f_len >= next_info):
            print(f"{(next_info * 100):.0f} %")
            next_info += info_increment
        f_count = f_count + 1

    print("Done")


if __name__ == "__main__":
    main()
