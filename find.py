import argparse
import config
import persistance
import re
import os
import shutil
import subprocess


def build_filename_map(directory):
    filename_map = {}
    for filename in os.listdir(directory):
        file_path = os.path.join(directory, filename)
        if os.path.isfile(file_path):
            filename_map[os.path.splitext(filename)[0]] = file_path
    return filename_map


parser = argparse.ArgumentParser(description='Meme Searcher')
parser.add_argument('searchstring')
args = parser.parse_args()

# empty found dir
filelist = [f for f in os.listdir(config.found_dir)]
for f in filelist:
    os.remove(os.path.join(config.found_dir, f))

memes = build_filename_map(config.meme_dir)

found = False
for data in persistance.load_all():

    texts = []
    for attr in data:
        if isinstance(data[attr], list):
            texts.extend(data[attr])
        else:
            texts.append(data[attr])

    if any([text for text in texts if re.search(f".*{args.searchstring}.*", text, re.IGNORECASE)]):
        file = memes[data["id"]]
        dest_file = os.path.join(
            config.found_dir, data["id"]) + os.path.splitext(file)[1]
        shutil.copyfile(file, dest_file)
        found = True

if found:
    subprocess.Popen(rf'explorer "{config.found_dir}\"')
