import os

from PIL import ImageQt, Image
from PyQt5.QtCore import QObject, QRectF, Qt
from PyQt5.QtGui import QPixmap

from src.model.image import *
import shutil

from PyQt5.QtWidgets import QFileDialog, QMainWindow, QGraphicsView, QGraphicsScene
from src.view.main_sense import *

projects_dest = '/home/sijie/Desktop/GUI/stock/projects'


def get_images_from_dir(path):
    ret = []
    for _, _, filenames in os.walk(path):
        for filename in filenames:
            if filename.endswith(('.png', '.xpm', '.jpg')):
                ret.append(filename)
    return ret


class MainSenseController(QMainWindow, Ui_MainWindow):
    project_name = 'test'
    project_dest = os.path.join(projects_dest, project_name)

    label_dest = os.path.join(project_dest, 'label')

    print(project_dest)
    print(label_dest)

    def __init__(self):
        super(MainSenseController, self).__init__()

        self.setupUi(self)
        self.update()
        self.action_project_add_files.triggered.connect(self.open_file_names_dialog)
        self.push_button_add_files.clicked.connect(self.open_file_names_dialog)
        self.images_list_widget.itemSelectionChanged.connect(self.selection_handler)
        self.action_file_zoom_in.triggered.connect(lambda: self.zoom_handler(0))
        self.action_file_zoom_out.triggered.connect(lambda: self.zoom_handler(1))

    # TODO may change to model build-in method
    def update(self):
        self.images_list_widget.clear()
        self.images_list_widget.addItems(get_images_from_dir(self.label_dest))

    def open_file_names_dialog(self):
        options = QFileDialog.Options()
        options |= QFileDialog.DontUseNativeDialog
        files, _ = QFileDialog.getOpenFileNames(None, "choose images", "",
                                                "Images (*.png *.xpm *.jpg)", options=options)
        if files:
            print(files)

            # copy files to the project label folder
            for file in files:
                shutil.copy2(file, self.label_dest)

            self.update()

    def selection_handler(self):
        scene = QGraphicsScene()

        items = [item.text() for item in self.images_list_widget.selectedItems()]
        image_name = os.path.join(self.label_dest, items[0])

        img = Image.open(image_name)

        scene.clear()
        img_q = ImageQt.ImageQt(img)
        pix_map = QPixmap.fromImage(img_q)
        scene.addPixmap(pix_map)
        # w, h = img.size
        # self.graphics_view.fitInView(QRectF(0, 0, w, h), Qt.KeepAspectRatio)

        self.graphics_view.setScene(scene)
        self.graphics_view.show()

    def zoom_handler(self, mode):
        # TODO add wheel event
        # TODO default size
        if mode == 0:
            self.graphics_view.scale(1.1, 1.1)
        else:
            self.graphics_view.scale(1/1.1, 1/1.1)

if __name__ == "__main__":
    import sys

    app = QtWidgets.QApplication(sys.argv)
    application = MainSenseController()
    application.show()
    sys.exit(app.exec_())
