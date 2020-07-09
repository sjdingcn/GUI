#!/usr/bin/env python
# coding: utf-8

# # Mask R-CNN - Inspect Ballon Trained Model
# 
# Code and visualizations to test, debug, and evaluate the Mask R-CNN model.


import json
import os
import sys

import cv2 as cv
import mrcnn.model as modellib
import numpy as np
import tensorflow as tf
from PIL import Image

import src.model.project as project

# Root directory of the project
ROOT_DIR = os.path.abspath("")

# Import Mask RCNN
sys.path.append(ROOT_DIR)  # To find local version of the library


def detect(project_dir, model_dir, weight_name):
    # TODO: optimize the code
    label_dir = os.path.join(project_dir, 'label')

    config = project.ProjectConfig()

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
    # TODO: code for 'training' test mode not ready yet
    TEST_MODE = "inference"

    # ## Load Model

    # Create model in inference mode
    with tf.device(DEVICE):
        model = modellib.MaskRCNN(mode="inference", model_dir=model_dir,
                                  config=config)

    weights_path = os.path.join(model_dir, weight_name)

    print("Loading weights ", weights_path)
    model.load_weights(weights_path, by_name=True)
    data = {}
    for root, _, filenames in os.walk(label_dir):
        for filename in filenames:
            if filename.endswith(('.png', '.xpm', '.jpg')):
                image = np.asarray(Image.open(os.path.join(root, filename)))
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
                # cv.imshow("test", img)
                # cv.waitKey()
                # print(masks[k])
                contours, hierarchy = cv.findContours(img, cv.RETR_EXTERNAL, cv.CHAIN_APPROX_SIMPLE)
                for c in contours:
                    # cv.drawContours(img, [c], -1, (255, 0, 0), 3)
                    # print(c)

                    region = {"shape_attributes": {"name": "polygon", "all_points_x": c[:, 0, 0].tolist(),
                                                   "all_points_y": c[:, 0, 1].tolist()},
                              "region_attributes": {"Attribute": ""}}
                    regions.append(region)
                path = os.path.join(label_dir, filename)

                size = os.stat(path).st_size
                key = filename + str(size)

                data[key] = {"filename": filename, "size": size, "regions": regions, "file_attributes": {}}

        with open(os.path.join(label_dir, 'data.json'), 'w') as outfile:
            json.dump(data, outfile)
