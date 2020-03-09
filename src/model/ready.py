import copy
import json
import os
import os.path
import random
import shutil

from PIL import Image


# TODO: optimize the code
# TODO: support more image format and size
# TODO: more error cases
class Ready:
    def __init__(self, project_dir):
        # img_path = gb.glob("/home/sijie/Desktop/GUI/stock/projects/test/label/*.png")
        self.data_dir = os.path.join(project_dir, 'data')
        self.label_dir = os.path.join(project_dir, 'label')

    def image_rotate(self):
        for parent, dirnames, filenames in os.walk(self.label_dir):
            print("test")
            for filename in filenames:
                if filename.endswith('.png'):
                    print('parent is :' + parent)
                    print('filename is :' + filename)
                    currentPath = os.path.join(parent, filename)
                    print('the fulll name of the file is :' + currentPath)

                    img = Image.open(currentPath)
                    # print (img.format, img.size, img.mode)

                    # # cut into 1024*1024
                    # box1 = (448 + 50, 28, 1472 + 50, 1052)
                    # image1 = img.crop(box1)
                    #
                    # # zoom into 512*512
                    # image1.thumbnail((512, 512))

                    # img.show("cut", image1)
                    # cv2.waitKey(0)
                    # image1.save(r"/home/gemc/Desktop/Sijie/ALCUBrass/photoscut/" + filename)
                    # rotation
                    transposed90 = img.transpose(Image.ROTATE_90)
                    transposed180 = img.transpose(Image.ROTATE_180)
                    transposed270 = img.transpose(Image.ROTATE_270)
                    name, suffix = os.path.splitext(filename)
                    # # print(name)
                    img.save(os.path.join(self.data_dir, name + ".png"))
                    transposed90.save(os.path.join(self.data_dir, name + "(1).png"))
                    transposed180.save(os.path.join(self.data_dir, name + "(2).png"))
                    transposed270.save(os.path.join(self.data_dir, name + "(3).png"))

    def json_rotate(self):
        all_data = {}
        with open(os.path.join(self.label_dir, 'data.json')) as json_file:
            data = json.load(json_file)
        for _, _, filenames in os.walk(self.label_dir):
            for filename in filenames:
                if filename.endswith('.png'):
                    size = os.stat(os.path.join(self.data_dir, filename)).st_size
                    key = filename + str(size)
                    # print(key)
                    name, suffix = os.path.splitext(filename)
                    regions = data[key]["regions"]

                    regions1, regions2, regions3 = [], [], []
                    for x in regions:
                        temp1 = copy.deepcopy(x)
                        temp2 = copy.deepcopy(x)
                        temp3 = copy.deepcopy(x)
                        all_points_x_rotate = [512 - i for i in x["shape_attributes"]["all_points_x"]]
                        all_points_y_rotate = [512 - i for i in x["shape_attributes"]["all_points_y"]]
                        all_points_x = x["shape_attributes"]["all_points_x"]
                        all_points_y = x["shape_attributes"]["all_points_y"]

                        temp1["shape_attributes"]["all_points_x"] = all_points_y
                        temp1["shape_attributes"]["all_points_y"] = all_points_x_rotate
                        regions1.append(temp1)

                        temp2["shape_attributes"]["all_points_x"] = all_points_x_rotate
                        temp2["shape_attributes"]["all_points_y"] = all_points_y_rotate
                        regions2.append(temp2)

                        temp3["shape_attributes"]["all_points_x"] = all_points_y_rotate
                        temp3["shape_attributes"]["all_points_y"] = all_points_x
                        regions3.append(temp3)

                    filename1 = name + "(1).png"
                    filename2 = name + "(2).png"
                    filename3 = name + "(3).png"
                    size1 = os.stat(os.path.join(self.data_dir, filename1)).st_size
                    size2 = os.stat(os.path.join(self.data_dir, filename2)).st_size
                    size3 = os.stat(os.path.join(self.data_dir, filename3)).st_size
                    # print(os.path.join(self.data_dir, filename3))
                    key1 = filename1 + str(size1)
                    key2 = filename2 + str(size2)
                    key3 = filename3 + str(size3)
                    all_data[key] = {"filename": filename, "size": size, "regions": regions, "file_attributes": {}}
                    all_data[key1] = {"filename": filename1, "size": size1, "regions": regions1, "file_attributes": {}}
                    all_data[key2] = {"filename": filename2, "size": size2, "regions": regions2, "file_attributes": {}}
                    all_data[key3] = {"filename": filename3, "size": size3, "regions": regions3, "file_attributes": {}}
                    # break
        # json_data = json.dumps(all_data)
        # print(json_data)
        train = {}
        val = {}
        test = {}
        # print(all_data)
        # print(len(list(all_data.items())))
        # write val json file
        print("val")
        for i in range(0, 12):
            data_key, data_value = random.choice(list(all_data.items()))
            val[data_key] = data_value
            all_data.pop(data_key)
            name = data_key.split(".png")[0] + ".png"
            # print(name)
            source = os.path.join(self.data_dir, name)
            destination = os.path.join(self.data_dir, 'val', name)
            shutil.move(source, destination)
        with open(os.path.join(self.data_dir, 'val', 'new.json'), 'w') as outfile:
            json.dump(val, outfile)

        # write test json file
        print("test")
        for i in range(0, 12):
            data_key, data_value = random.choice(list(all_data.items()))
            test[data_key] = data_value
            all_data.pop(data_key)
            name = data_key.split(".png")[0] + ".png"
            # print(name)
            source = os.path.join(self.data_dir, name)
            destination = os.path.join(self.data_dir, 'test', name)
            shutil.move(source, destination)
        with open(os.path.join(self.data_dir, 'test', 'new.json'), 'w') as outfile:
            json.dump(test, outfile)

        # write train json file
        train = all_data.copy()
        source = self.data_dir
        destination = os.path.join(self.data_dir, 'train')
        files = os.listdir(source)
        for f in files:
            if f.endswith('.png'):
                shutil.move(os.path.join(self.data_dir, f), destination)
        with open(os.path.join(self.data_dir, 'train', 'new.json'), 'w') as outfile:
            json.dump(train, outfile)

# if __name__ == "__main__":
#     main(sys.argv)
