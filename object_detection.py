# https://dontrepeatyourself.org/post/object-detection-with-python-deep-learning-and-opencv/

import cv2
import config
from persistance import load_data, save_data
import os


def main():
    # find all non tagged images
    data_files = os.listdir(config.processed_meme_dir)
    files_objects_missing = [load_data(os.path.splitext(file)[
        0]) for file in data_files if "objects" not in load_data(os.path.splitext(file)[0])]

    # could be a lengthy operation some feedback
    f_count = 0
    f_len = len(files_objects_missing)
    info_increment = 0.1
    next_info = info_increment

    for data in files_objects_missing:
        file = data["id"] + ".tiff"
        path = os.path.join(config.processed_meme_dir, file)

        # get image
        image = cv2.imread(path)
        image = cv2.resize(image, (640, 480))

        # load net
        weights = "ssd_mobilenet/frozen_inference_graph.pb"
        model = "ssd_mobilenet/ssd_mobilenet_v3_large_coco_2020_01_14.pbtxt"
        net = cv2.dnn.readNetFromTensorflow(weights, model)

        # get classes
        class_names = []
        with open("ssd_mobilenet/coco_names.txt", "r") as f:
            class_names = f.read().strip().split("\n")

        blob = cv2.dnn.blobFromImage(
            image, 1.0/127.5, (320, 320), [127.5, 127.5, 127.5])
        net.setInput(blob)

        # predict
        output = net.forward()

        # gather results
        res = list(set([class_names[int(detection[1]) - 1]
                   for detection in output[0, 0, :, :] if detection[2] > 0.5]))
        
        data["objects"] = res
        save_data(data)

        # feedback
        if (f_count/f_len >= next_info):
            print(f"{(next_info * 100):.0f} %")
            next_info += info_increment

        f_count = f_count + 1


if __name__ == "__main__":
    main()
