"""
Mask R-CNN
Train on the toy Balloon dataset and implement color splash effect.

Copyright (c) 2018 Matterport, Inc.
Licensed under the MIT License (see LICENSE for details)
Written by Waleed Abdulla


"""

import os
import sys
import json
import datetime
import numpy as np
import skimage.draw
import imgaug
import colorsys

# Root directory of the project
# ROOT_DIR = os.path.abspath("")
ROOT_DIR = '/home/sijie/Desktop/GUI/stock/projects/test'
# Import Mask RCNN
sys.path.append(ROOT_DIR)  # To find local version of the library
from mrcnn.config import Config
from mrcnn import model as modellib, utils

# Path to trained weights file
COCO_WEIGHTS_PATH = os.path.join(ROOT_DIR, "mask_rcnn_coco.h5")

# Directory to save logs and model checkpoints, if not provided
# through the command line argument --logs
DEFAULT_LOGS_DIR = os.path.join(ROOT_DIR, "logs")


############################################################
#  Configurations
############################################################


class projectConfig(Config):
    """Configuration for training on the toy  dataset.
    Derives from the base Config class and overrides some values.
    """
    # Give the configuration a recognizable name
    NAME = "project"

    # We use a GPU with 12GB memory, which can fit two images.
    # Adjust down if you use a smaller GPU.
    IMAGES_PER_GPU = 3

    # TODO
    # Number of classes (including background)
    NUM_CLASSES = 1 + 1 + 1 + 1  # Background + AL + CU + Brass

    # Number of training steps per epoch
    STEPS_PER_EPOCH = 100

    # TODO adjust this
    DETECTION_MIN_CONFIDENCE = 0.5
    # TODO image dimension
    IMAGE_MIN_DIM = 512
    IMAGE_MAX_DIM = 512
    RPN_ANCHOR_SCALES = (8, 16, 32, 64, 128)
    TRAIN_ROIS_PER_IMAGE = 64


############################################################
#  Dataset
############################################################

class projectDataset(utils.Dataset):
    # TODO
    def load_project(self, datasetDir, subset):
        # Setup classes
        self.add_class("Attribute", 1, "AL")
        self.add_class("Attribute", 2, "CU")
        self.add_class("Attribute", 3, "Brass")
        # Create dataset path
        # assert subset in ["train", "val", "test"]
        datasetDir = os.path.join(datasetDir, subset)
        # Read dataset information from the json file
        jsonData = json.load(open(os.path.join(datasetDir, "new.json")))
        # Transfer dict to list
        jsonData = list(jsonData.values())
        # Load images and add them to the dataset
        for data in jsonData:

            imagePath = os.path.join(datasetDir, data["filename"])
            image = skimage.io.imread(imagePath)
            height, width = image.shape[:2]
            if len(data["regions"]) > 1:
                self.add_image(
                    "Attribute",
                    image_id=data["filename"],
                    path=imagePath,
                    width=width,
                    height=height,
                    regions=data["regions"])

    def load_mask(self, image_id):
        imageInfo = self.image_info[image_id]
        regions = imageInfo["regions"]
        masks = np.zeros(
            [imageInfo["height"], imageInfo["width"], len(imageInfo["regions"])], dtype=np.uint8)
        classIds = np.zeros(len(imageInfo["regions"]), dtype=np.int32)
        for index, region in enumerate(regions):
            rr, cc = skimage.draw.polygon(
                region["shape_attributes"]["all_points_y"],
                region["shape_attributes"]["all_points_x"])
            masks[rr, cc, index] = 1
            # TODO
            if region["region_attributes"]["Attribute"] == "AL":
                classIds[index] = 1
            elif region["region_attributes"]["Attribute"] == "CU":
                classIds[index] = 2
            elif region["region_attributes"]["Attribute"] == "Brass":
                classIds[index] = 3
        return masks.astype(np.bool), classIds

    def image_reference(self, image_id):
        """Return the path of the image."""
        info = self.image_info[image_id]
        if info["source"] == "Attribute":
            return info["path"]
        else:
            super(self.__class__, self).image_reference(image_id)


def train(model):
    """Train the model."""
    # Training dataset.
    dataset_train = projectDataset()
    dataset_train.load_project(args.dataset, "train")
    dataset_train.prepare()

    # Validation dataset
    dataset_val = projectDataset()
    dataset_val.load_project(args.dataset, "val")
    dataset_val.prepare()

    # Flip the image 50% of time
    augmentation = imgaug.augmenters.Fliplr(0.5)
    # TODO
    # Training - Stage 1
    model.train(dataset_train, dataset_val,
                learning_rate=config.LEARNING_RATE,
                epochs=80,  # 40,
                layers='heads',
                augmentation=augmentation)

    # Training - Stage 2
    # Finetune layers from ResNet stage 4 and up
    print("Fine tune Resnet stage 4 and up")
    model.train(dataset_train, dataset_val,
                learning_rate=config.LEARNING_RATE,
                epochs=240,  # 120,
                layers='4+',
                augmentation=augmentation)

    # Training - Stage 3
    # Fine tune all layers
    print("Fine tune all layers")
    model.train(dataset_train, dataset_val,
                learning_rate=config.LEARNING_RATE / 10,
                epochs=400,  # 160,
                layers='all',
                augmentation=augmentation)



############################################################
#  Training
############################################################

if __name__ == '__main__':
    import argparse

    # Parse command line arguments
    parser = argparse.ArgumentParser(
        description='Train Mask R-CNN to detect project.')
    parser.add_argument('--dataset', required=False,
                        metavar="/path/to/project/dataset/",
                        help='Directory of the project dataset')
    parser.add_argument('--weights', required=True,
                        metavar="/path/to/weights.h5",
                        help="Path to weights .h5 file or 'coco'")
    parser.add_argument('--format', required=False,
                        metavar="RGB",
                        help='RGB or RGB-D')
    args = parser.parse_args()

    # Validate arguments
    assert args.dataset, "Argument --dataset is required for training"
    print("Weights: ", args.weights)
    print("Dataset: ", args.dataset)
    print("Logs: ", args.logs)

    # Configurations
    config = projectConfig()
    config.display()

    # Create model
    model = modellib.MaskRCNN(mode="training", config=config,
                              model_dir=args.logs)


    # Select weights file to load
    if args.weights.lower() == "coco":
        weights_path = COCO_WEIGHTS_PATH
        # Download weights file
        if not os.path.exists(weights_path):
            utils.download_trained_weights(weights_path)
    elif args.weights.lower() == "last":
        # Find last trained weights
        weights_path = model.find_last()
    elif args.weights.lower() == "imagenet":
        # Start from ImageNet trained weights
        weights_path = model.get_imagenet_weights()
    else:
        weights_path = args.weights

    # Load weights
    print("Loading weights ", weights_path)
    if args.weights.lower() == "coco":
        # Exclude the last layers because they require a matching
        # number of classes
        model.load_weights(weights_path, by_name=True, exclude=[
            "mrcnn_class_logits", "mrcnn_bbox_fc",
            "mrcnn_bbox", "mrcnn_mask"])
    else:
        model.load_weights(weights_path, by_name=True)
        # model.load_weights(weights_path, by_name=True, exclude=[
        #     "mrcnn_class_logits", "mrcnn_bbox_fc",
        #     "mrcnn_bbox", "mrcnn_mask", "conv1"])

    # Train or evaluate
    if args.command == "train":
        train(model)
    # elif args.command == "splash":
    #     detect_and_color_splash(model, image_path=args.image,
    #                             video_path=args.video)
    else:
        print("'{}' is not recognized. "
              "Use 'train' or 'splash'".format(args.command))