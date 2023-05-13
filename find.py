import argparse
import config
import persistance
import re
import os
import shutil
import subprocess

parser = argparse.ArgumentParser(description='Meme Searcher')
parser.add_argument('searchstring')
args = parser.parse_args()

# empty found dir
filelist = [f for f in os.listdir(config.found_dir)]
for f in filelist:
    os.remove(os.path.join(config.found_dir, f))

found = False
for data in persistance.load_all():

    text = data["tags"]
    text.append(data["text"])

    if any([x for x in text if re.search(f".*{args.searchstring}.*", x)]):
        file = os.path.join(config.processed_meme_dir, data["id"]) + ".tiff"
        dest_file = os.path.join(config.found_dir, data["id"]) + ".tiff"
        shutil.copyfile(file, dest_file)
        found = True

if found:
    subprocess.Popen(rf'explorer "{config.found_dir}\"')