import json
import random
import shutil
from pathlib import Path


def ready(data_dir, label_dir, total):
    with open(Path(label_dir, 'data.json')) as json_file:
        data = json.load(json_file)

    val = {}
    test = {}

    # write val json file
    print("val")
    for i in range(0, total // 10):
        data_key, data_value = random.choice(list(data.items()))
        val[data_key] = data_value
        data.pop(data_key)
        name = data_value['filename']
        source = Path(label_dir, name)
        destination = Path(data_dir, 'val', name)
        shutil.copy2(source, destination)
    with open(Path(data_dir, 'val', 'new.json'), 'w') as outfile:
        json.dump(val, outfile)

    # write test json file
    print("test")
    for i in range(0, total // 10):
        data_key, data_value = random.choice(list(data.items()))
        test[data_key] = data_value
        data.pop(data_key)
        name = data_value['filename']
        source = Path(label_dir, name)
        destination = Path(data_dir, 'test', name)
        shutil.copy2(source, destination)
    with open(Path(data_dir, 'test', 'new.json'), 'w') as outfile:
        json.dump(test, outfile)

    # write train json file
    train = data.copy()
    for data_key, data_value in list(train.items()):
        name = data_value['filename']
        source = Path(label_dir, name)
        destination = Path(data_dir, 'train', name)
        shutil.copy2(source, destination)
    with open(Path(data_dir, 'train', 'new.json'), 'w') as outfile:
        json.dump(train, outfile)
