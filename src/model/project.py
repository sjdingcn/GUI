"""
Mask R-CNN
Train on the toy Balloon dataset and implement color splash effect.

Copyright (c) 2018 Matterport, Inc.
Licensed under the MIT License (see LICENSE for details)
Written by Waleed Abdulla


"""

import json
import os

import imgaug
import numpy as np
import skimage.draw
from mrcnn import model as modellib, utils
from mrcnn.config import Config

from src.view.utils import gui_root

# Path to trained weights file
WEIGHT = 'coco'
FORMAT = 'RGB'


############################################################
#  Configurations
############################################################

# TODO
class ProjectConfig(Config):
    """Configuration for training on the toy  dataset.
    Derives from the base Config class and overrides some values.
    """
    # Give the configuration a recognizable name
    NAME = "project"

    # We use a GPU with 12GB memory, which can fit two images.
    # Adjust down if you use a smaller GPU.
    IMAGES_PER_GPU = 3

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
    if FORMAT == 'RGB-D':
        IMAGE_CHANNEL_COUNT = 4
        MEAN_PIXEL = np.array([123.7, 116.8, 103.9, 220])


############################################################
#  Dataset
############################################################

class ProjectDataset(utils.Dataset):
    def __init__(self, attributes):

        super().__init__()
        self.attributes = attributes

    
    def load_image(self, image_id):
        """Load RGB or RGB-D images.
        """
        # Load image
        image = skimage.io.imread(self.image_info[image_id]['path'])
        # TODO N channels
        # If grayscale. Convert to RGB for consistency.
        if image.ndim != 3:
            image = skimage.color.gray2rgb(image)
        # If has an alpha channel, keep it.
        if image.shape[-1] == 4:
            pass
        return image

    def load_project(self, dataset_dir, subset):
        # Setup classes
        for attribute in self.attributes:
            i = 1
            self.add_class("Attribute", i, attribute)
            i += 1

        # Create dataset path
        # assert subset in ["train", "val", "test"]
        dataset_dir = os.path.join(dataset_dir, subset)
        # Read dataset information from the json file
        json_data = json.load(open(os.path.join(dataset_dir, "new.json")))
        # Transfer dict to list
        json_data = list(json_data.values())
        # Load images and add them to the dataset
        for data in json_data:

            image_path = os.path.join(dataset_dir, data["filename"])
            image = skimage.io.imread(image_path)
            height, width = image.shape[:2]
            if len(data["regions"]) > 1:
                self.add_image(
                    "Attribute",
                    image_id=data["filename"],
                    path=image_path,
                    width=width,
                    height=height,
                    regions=data["regions"])

    def load_mask(self, image_id):
        image_info = self.image_info[image_id]
        regions = image_info["regions"]
        masks = np.zeros(
            [image_info["height"], image_info["width"], len(image_info["regions"])], dtype=np.uint8)
        class_ids = np.zeros(len(image_info["regions"]), dtype=np.int32)
        for index, region in enumerate(regions):
            rr, cc = skimage.draw.polygon(
                region["shape_attributes"]["all_points_y"],
                region["shape_attributes"]["all_points_x"])
            masks[rr, cc, index] = 1
            for i, attribute in enumerate(self.attributes):

                if region["region_attributes"]["Attribute"] == attribute:
                    class_ids[index] = i

        return masks.astype(np.bool), class_ids

    def image_reference(self, image_id):
        """Return the path of the image."""
        info = self.image_info[image_id]
        if info["source"] == "Attribute":
            return info["path"]
        else:
            super(self.__class__, self).image_reference(image_id)


# TODO
def train(model):
    """Train the model."""
    # Training dataset.
    dataset_train = ProjectDataset(list(args.attributes.split(",")))
    dataset_train.load_project(args.dataset, "train")
    dataset_train.prepare()

    # Validation dataset
    dataset_val = ProjectDataset(list(args.attributes.split(",")))
    dataset_val.load_project(args.dataset, "val")
    dataset_val.prepare()

    # Flip the image 50% of time
    # augmentation = imgaug.augmenters.Fliplr(0.5)
    augmentation = imgaug.augmenters.Rot90(imgaug.ALL, keep_size=False)

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

    parser.add_argument('--dataset', required=True,
                        metavar="/path/to/project/dataset/",
                        help='Directory of the project dataset')

    parser.add_argument('--logs', required=False,
                        # default=DEFAULT_LOGS_DIR,
                        metavar="/path/to/logs/",
                        help='Logs and checkpoints directory (default=logs/)')
    parser.add_argument('--attributes', required=True,
                        metavar="[]",
                        help="type in attributes as a list")

    args = parser.parse_args()

    # Validate arguments
    assert args.dataset, "Argument --dataset is required for training"

    print("Weights: ", WEIGHT)
    print("Dataset: ", args.dataset)
    print("Logs: ", args.logs)
    print("Attributes: ", list(args.attributes.split(",")))
    print("Format: ", FORMAT)

    # Configurations
    config = ProjectConfig()
    config.display()

    # Create model
    model = modellib.MaskRCNN(mode="training", config=config, model_dir=args.logs)

    # Select weights file to load
    if WEIGHT.lower() == "coco":
        weights_path = os.path.join(str(gui_root()), "stock", "mask_rcnn_coco.h5")
        # Download weights file
        if not os.path.exists(weights_path):
            utils.download_trained_weights(weights_path)
    elif WEIGHT.lower() == "last":
        # Find last trained weights
        weights_path = model.find_last()
    elif WEIGHT.lower() == "imagenet":
        # Start from ImageNet trained weights
        weights_path = model.get_imagenet_weights()
    else:
        weights_path = args.weights

    # Load weights
    print("Loading weights ", weights_path)
    if WEIGHT.lower() == "coco":
        # Exclude the last layers because they require a matching
        # number of classes
        model.load_weights(weights_path, by_name=True, exclude=[
            "mrcnn_class_logits", "mrcnn_bbox_fc",
            "mrcnn_bbox", "mrcnn_mask"])
    else:
        if FORMAT.lower() == "RGB":
            model.load_weights(weights_path, by_name=True)
        else:
            model.load_weights(weights_path, by_name=True, exclude=[
                "mrcnn_class_logits", "mrcnn_bbox_fc",
                "mrcnn_bbox", "mrcnn_mask", "conv1"])

    train(model)
