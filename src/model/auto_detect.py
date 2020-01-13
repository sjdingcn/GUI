#!/usr/bin/env python
# coding: utf-8

# # Mask R-CNN - Inspect Ballon Trained Model
# 
# Code and visualizations to test, debug, and evaluate the Mask R-CNN model.


import os
import sys

from PIL import Image
import matplotlib.pyplot as plt
import tensorflow as tf
import mrcnn.model as modellib
from mrcnn import visualize

import src.model.project as project
from src.view.main_sense_controller import ProjectInfo
import numpy as np

import cv2 as cv
import json

import time

# Root directory of the project
ROOT_DIR = os.path.abspath("")

# Import Mask RCNN
sys.path.append(ROOT_DIR)  # To find local version of the library

# Directory to save logs and trained model
MODEL_DIR = os.path.join(ProjectInfo().auto_detect_dest)
# Path to Ballon trained weights

# ## Configurations


config = project.projectConfig()
project_DIR = ProjectInfo().project_dest
label_DIR = ProjectInfo().label_dest


# Override the training configurations with a few
# changes for inferencing.
class InferenceConfig(config.__class__):
    # Run detection on one image at a time
    GPU_COUNT = 1
    IMAGES_PER_GPU = 1


config = InferenceConfig()
config.display()

# ## Notebook Preferences

# In[4]:


# Device to load the neural network on.
# Useful if you're training a model on the same 
# machine, in which case use CPU and leave the
# GPU for training.
DEVICE = "/gpu:0"  # /cpu:0 or /gpu:0

# Inspect the model in training or inference modes
# values: 'inference' or 'training'
# TODO: code for 'training' test mode not ready yet
TEST_MODE = "inference"

# ## Load Model

# Create model in inference mode
with tf.device(DEVICE):
    model = modellib.MaskRCNN(mode="inference", model_dir=MODEL_DIR,
                              config=config)


def auto_detection(auto_detect_name):
    weights_path = os.path.join(MODEL_DIR, auto_detect_name)

    print("Loading weights ", weights_path)
    model.load_weights(weights_path, by_name=True)
    data = {}
    for root, _, filenames in os.walk(label_DIR):
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
                              "region_attributes": {"Attribute": "id"}}
                    regions.append(region)
                path = os.path.join(label_DIR, filename)

                size = os.stat(path).st_size
                key = filename + str(size)

                data[key] = {"filename": filename, "size": size, "regions": regions, "file_attributes": {}}

        with open(os.path.join(label_DIR, 'data.json'), 'w') as outfile:
            json.dump(data, outfile)
