import json
import os
import config

def load_data(id):
    file_path = os.path.join(config.data_dir, id) + ".json"
    if os.path.isfile(file_path):
        f = open(file_path)
        return json.load(f)
    else:
        return {"id": id}


def save_data(data):
    path = f"{os.path.join(config.data_dir, data['id'])}.json"
    with open(path, 'w') as f:
        json.dump(data, f, indent=4, sort_keys=True)
