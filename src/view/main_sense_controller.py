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
        try:
            self.list_widget_images_update()
            self.label_page_id_update()
            self.graphics_view_update()
        except:
            pass

        self.action_project_add_files.triggered.connect(self.open_file_names_dialog)
        self.push_button_add_files.clicked.connect(self.open_file_names_dialog)
        self.list_widget_images.itemSelectionChanged.connect(self.selection_handler)
        self.action_file_zoom_in.triggered.connect(lambda: self.zoom_handler(0))
        self.action_file_zoom_out.triggered.connect(lambda: self.zoom_handler(1))
        self.button_previous_page.clicked.connect(lambda: self.page_turning_handler(0))
        self.button_next_page.clicked.connect(lambda: self.page_turning_handler(1))

    # TODO may change to model build-in method
    def list_widget_images_update(self):

        self.list_widget_images.clear()
        self.list_widget_images.addItems(get_images_from_dir(self.label_dest))
        self.list_widget_images.setCurrentRow(0)

        print(self.list_widget_images.currentRow())
        print(self.list_widget_images.currentItem().text())

        # self.graphics_view_update()

    def graphics_view_update(self):
        scene = QGraphicsScene()

        item = self.list_widget_images.currentItem()

        print(self.list_widget_images.currentRow())
        print(self.list_widget_images.currentItem().text())


        image_name = os.path.join(self.label_dest, item.text())

        img = Image.open(image_name)

        scene.clear()
        img_q = ImageQt.ImageQt(img)
        pix_map = QPixmap.fromImage(img_q)
        scene.addPixmap(pix_map)
        # w, h = img.size
        # self.graphics_view.fitInView(QRectF(0, 0, w, h), Qt.KeepAspectRatio)
        print(self.graphics_view.setScene(scene))
        print(self.graphics_view.show())



    def label_page_id_update(self):

        self.label_page_id.setText(str(self.list_widget_images.currentRow() + 1)
                                   + ' / ' + str(self.list_widget_images.count()))

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

            self.list_widget_images_update()

    def selection_handler(self):

        # items = [item for item in self.list_widget_images.selectedItems()]
        # if items is not None:
        #     self.list_widget_images.setCurrentItem(items[0])

        self.label_page_id_update()
        self.graphics_view_update()

    def zoom_handler(self, mode):
        # TODO add wheel event
        # TODO default size
        if mode == 0:
            self.graphics_view.scale(1.1, 1.1)
        else:
            self.graphics_view.scale(1 / 1.1, 1 / 1.1)

    def page_turning_handler(self, mode):
        if mode == 0 and 0 < self.list_widget_images.currentRow() <= self.list_widget_images.count() - 1:

            self.list_widget_images.setCurrentRow(self.list_widget_images.currentRow() - 1)
        elif mode == 1 and 0 <= self.list_widget_images.currentRow() < self.list_widget_images.count() - 1:
            self.list_widget_images.setCurrentRow(self.list_widget_images.currentRow() + 1)
        else:
            pass
        self.label_page_id_update()


if __name__ == "__main__":
    import sys

    app = QtWidgets.QApplication(sys.argv)
    application = MainSenseController()
    application.show()
    sys.exit(app.exec_())
