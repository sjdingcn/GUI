import json
import os
import random
import shutil
from pathlib import Path

from PyQt5.QtWidgets import QMessageBox


def gui_root() -> Path:
    """Returns gui root folder."""
    return Path(__file__).parent.parent


def ready(data_dir, label_dir, total):
    with open(Path(label_dir, 'data.json')) as json_file:
        data = json.load(json_file)

    val = {}
    test = {}

    # write val json file
    for i in range(0, total // 10):
        data_key, data_value = random.choice(list(data.items()))
        val[data_key] = data_value
        data.pop(data_key)
        name = data_value['filename']
        source = Path(label_dir, name)
        destination = Path(data_dir, 'val', name)
        shutil.copy2(source, destination)
    with open(Path(data_dir, 'val', 'data.json'), 'w') as outfile:
        json.dump(val, outfile)

    # write test json file
    for i in range(0, total // 10):
        data_key, data_value = random.choice(list(data.items()))
        test[data_key] = data_value
        data.pop(data_key)
        name = data_value['filename']
        source = Path(label_dir, name)
        destination = Path(data_dir, 'test', name)
        shutil.copy2(source, destination)
    with open(Path(data_dir, 'test', 'data.json'), 'w') as outfile:
        json.dump(test, outfile)

    # write train json file
    train = data.copy()
    for data_key, data_value in list(train.items()):
        name = data_value['filename']
        source = Path(label_dir, name)
        destination = Path(data_dir, 'train', name)
        shutil.copy2(source, destination)
    with open(Path(data_dir, 'train', 'data.json'), 'w') as outfile:
        json.dump(train, outfile)


def get_files_from_dir(path, mode):
    end = ()
    ret = []
    if mode == 'images':
        end = ('.png', '.xpm', '.jpg')
    elif mode == 'models':
        end = '.h5'
    else:
        pass
    for _, _, filenames in os.walk(path):
        for filename in filenames:
            if filename.endswith(end):
                ret.append(filename)
    return ret


def warning_msg_box(parent, text, informative_text):
    msg = QMessageBox(parent)
    msg.setIcon(QMessageBox.Warning)

    msg.setText(text)
    msg.setInformativeText(informative_text)
    msg.setWindowTitle("Warning")

    msg.setStandardButtons(QMessageBox.Ok)

    msg.exec_()


def detect(project_dir, model_dir, weight_name):
    import cv2 as cv
    import mrcnn.model as modellib
    import numpy as np
    import tensorflow as tf
    from PIL import Image

    import train_config

    label_dir = Path(project_dir, 'label')

    config = train_config.ProjectConfig()

    class InferenceConfig(config.__class__):
        # Run detection on one image at a time
        GPU_COUNT = 1
        IMAGES_PER_GPU = 1

    config = InferenceConfig()
    config.display()
    # Device to load the neural network on.
    # Useful if you're training a model on the same
    # machine, in which case use CPU and leave the
    # GPU for training.
    # TODO
    DEVICE = "/gpu:0"  # /cpu:0 or /gpu:0

    # Inspect the model in training or inference modes
    # values: 'inference' or 'training'
    TEST_MODE = "inference"

    # ## Load Model

    # Create model in inference mode
    with tf.device(DEVICE):
        model = modellib.MaskRCNN(mode="inference", model_dir=model_dir,
                                  config=config)

    weights_path = str(Path(model_dir, weight_name))

    print("Loading weights ", weights_path)
    model.load_weights(weights_path, by_name=True)
    data = {}
    for root, _, filenames in os.walk(label_dir):
        for filename in filenames:
            if filename.endswith(('.png', '.xpm', '.jpg')):
                image = np.asarray(Image.open(Path(root, filename)))
                results = model.detect([image], verbose=1)
                r = results[0]

                regions = []
                image = np.zeros((512, 512))
                # print(masks[k])
                mask_num = r['masks'].shape[2]
                for x in range(0, mask_num):
                    # print(x.shape)
                    if r['class_ids'][x] != 0:
                        for i in range(0, 512):
                            for j in range(0, 512):
                                if r['masks'][i, j, x]:
                                    image[i, j] = 1
                img = np.uint8(image * 255)

                contours, hierarchy = cv.findContours(img, cv.RETR_EXTERNAL, cv.CHAIN_APPROX_SIMPLE)
                for c in contours:
                    region = {"shape_attributes": {"name": "polygon", "all_points_x": c[:, 0, 0].tolist(),
                                                   "all_points_y": c[:, 0, 1].tolist()},
                              "region_attributes": {"Attribute": ""}}
                    regions.append(region)
                path = Path(label_dir, filename)

                size = os.stat(path).st_size
                key = filename + str(size)

                data[key] = {"filename": filename, "size": size, "regions": regions, "file_attributes": {}}

        with open(Path(label_dir, 'data.json'), 'w') as outfile:
            json.dump(data, outfile)


def clear_folder(dir):
    for f in [f for f in os.listdir(dir)]:
        os.remove(os.path.join(dir, f))
