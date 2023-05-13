import json
import os
import config


def load_all():
    data = []
    for file in [f for f in os.listdir(config.data_dir) if os.path.isfile(os.path.join(config.data_dir, f))]:
        data.append(load_data(os.path.splitext(file)[0]))
    return data


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
