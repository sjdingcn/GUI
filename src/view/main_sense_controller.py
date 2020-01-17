import json
import os

from PyQt5.QtGui import QPixmap, QImage, QPainter, QPen, QBrush, QPolygon, QPolygonF, QKeyEvent

import shutil

from PyQt5.QtWidgets import QFileDialog, QMainWindow, QGraphicsView, QGraphicsScene, QGraphicsItem, \
    QGraphicsSceneHoverEvent, QGraphicsPolygonItem, QGraphicsPixmapItem, QButtonGroup, QRadioButton
from prompt_toolkit.key_binding import KeyPress

from src.view.main_sense import *
# import src.model.auto_detect as auto

from PyQt5.QtCore import Qt, QPoint, QRectF, QSize


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


class ProjectInfo:
    def __init__(self):
        self.projects_dest = '/home/sijie/Desktop/GUI/stock/projects'
        self.project_name = 'test'
        self.project_dest = os.path.join(self.projects_dest, self.project_name)
        self.label_dest = os.path.join(self.project_dest, 'label')
        self.auto_detect_dest = os.path.join(self.project_dest, 'auto_detect')


class GUIPolygonItem(QGraphicsPolygonItem):
    def __init__(self, polygon):
        super().__init__(polygon)

    def keyPressEvent(self, event):
        if event.key() == Qt.Key_D:
            application.graphics_view.scene().removeItem(self)
            print('delete')

    def mousePressEvent(self, event):
        if event.button() == Qt.LeftButton and event.modifiers() == QtCore.Qt.ControlModifier:
            self.setSelected(True)
            print("select")


class GUIPixmapItem(QGraphicsPixmapItem):
    def __init__(self, pixmap):
        super().__init__(pixmap)
        self.points = []
        self.drawing = False
        self.start = False
        self.setAcceptHoverEvents(True)

    def mouseDoubleClickEvent(self, event):
        self.drawing = True
        self.start = True
        self.points.append(event.scenePos())

    def mousePressEvent(self, event):
        self.start = False

        if self.drawing:
            if event.button() == Qt.LeftButton:
                self.points.append(event.scenePos())
                self.update()
                print(event.scenePos().x())
            elif event.button() == Qt.RightButton:
                polygon_item = GUIPolygonItem(QPolygonF(self.points))
                polygon_item.setPen(QPen(Qt.yellow, 1, Qt.SolidLine))
                application.graphics_view.scene().addItem(polygon_item)

                polygon_item.setFlags(QGraphicsItem.ItemIsMovable | QGraphicsItem.ItemIsSelectable
                                      | QGraphicsItem.ItemIsFocusable)

                self.points.clear()
                self.drawing = False
            else:
                pass


    def hoverMoveEvent(self, event):
        if self.drawing:
            if len(self.points) > 1:
                self.points.pop()
            self.points.append(event.scenePos())
            print(event.scenePos())
            self.update()

    def paint(self, painter, option, widget):
        painter.drawPixmap(self.boundingRect().toRect(), self.pixmap())
        painter.setPen(QPen(Qt.yellow, 1, Qt.SolidLine))
        painter.drawConvexPolygon(QPolygonF(self.points))

    def wheelEvent(self, event):
        if event.modifiers() == QtCore.Qt.ControlModifier:
            if event.delta() == 120:
                MainSenseController.zoom_handler(application, 'zoom_in')

            elif event.delta() == -120:
                MainSenseController.zoom_handler(application, 'zoom_out')

            else:
                pass


class MainSenseController(QMainWindow, Ui_MainWindow):
    project_name = ProjectInfo().project_name
    project_dest = ProjectInfo().project_dest

    label_dest = ProjectInfo().label_dest
    auto_detect_dest = ProjectInfo().auto_detect_dest

    print(project_dest)
    print(label_dest)

    def __init__(self):
        super(MainSenseController, self).__init__()

        self.setupUi(self)
        try:
            self.list_widget_images_update()
            self.list_widget_models_update()
            self.label_page_id_update()
            self.graphics_view_update()
        except:
            pass

        # Controller for menu bar
        self.action_project_add_files.triggered.connect(self.open_file_names_dialog)
        self.action_project_remove_files.triggered.connect(self.remove_files_handler)
        self.action_file_zoom_in.triggered.connect(lambda: self.zoom_handler('zoom_in'))
        self.action_file_zoom_out.triggered.connect(lambda: self.zoom_handler('zoom_out'))
        self.action_file_default_size.triggered.connect(lambda: self.zoom_handler('default_size'))
        self.action_file_delete_polygon.triggered.connect(self.delete_polygon_handler)

        # Controller for list widget of images
        self.list_widget_images.itemSelectionChanged.connect(lambda: self.selection_handler('images'))
        self.push_button_add_images.clicked.connect(lambda: self.open_file_names_dialog('images'))
        self.push_button_remove_images.clicked.connect(lambda: self.remove_files_handler('images'))

        # Controller for list widget of models
        self.list_widget_models.itemSelectionChanged.connect(lambda: self.selection_handler('models'))
        self.push_button_add_models.clicked.connect(lambda: self.open_file_names_dialog('models'))
        self.push_button_remove_models.clicked.connect(lambda: self.remove_files_handler('models'))
        self.push_button_go.clicked.connect(self.go_handler)

        # Controller for graphic view
        self.button_previous_page.clicked.connect(lambda: self.page_turning_handler('previous_page'))
        self.button_next_page.clicked.connect(lambda: self.page_turning_handler('next_page'))

        # controller for manully tab
        self.push_button_add.clicked.connect(self.add_attribute_id)
        self.push_button_remove.clicked.connect(self.remove_attribute_id)



    def list_widget_images_update(self):

        self.list_widget_images.clear()
        self.list_widget_images.addItems(get_files_from_dir(self.label_dest, 'images'))
        self.list_widget_images.setCurrentRow(0)

    def list_widget_models_update(self):

        self.list_widget_models.clear()
        self.list_widget_models.addItems(get_files_from_dir(self.auto_detect_dest, 'models'))
        self.list_widget_models.setCurrentRow(0)

    def graphics_view_update(self):

        scene = QGraphicsScene(self.graphics_view)

        item = self.list_widget_images.currentItem()

        if item is not None:
            image_name = os.path.join(self.label_dest, item.text())
            scene.clear()
            with open(image_name, 'rb') as f:
                img = f.read()
            image = QImage.fromData(img)
            pix_map = QPixmap.fromImage(image)
            pixmap_item = GUIPixmapItem(pix_map)
            # pixmap_item.setPixmap(pix_map)
            scene.addItem(pixmap_item)

            # Read dataset information from the json file
            json_data = json.load(open(os.path.join(self.label_dest, "data.json")))

            # Transfer dict to list
            json_data = list(json_data.values())
            polygons = self.json2polygons(json_data, item.text())

            for polygon in polygons:
                polygon_item = GUIPolygonItem(polygon)
                polygon_item.setPen(QPen(Qt.yellow, 1, Qt.SolidLine))
                scene.addItem(polygon_item)

                polygon_item.setFlags(QGraphicsItem.ItemIsMovable | QGraphicsItem.ItemIsSelectable
                                      | QGraphicsItem.ItemIsFocusable)

            print('polygons')
        else:
            scene.clear()

        self.graphics_view.setScene(scene)

        self.graphics_view.show()

    def label_page_id_update(self):

        self.label_page_id.setText(str(self.list_widget_images.currentRow() + 1)
                                   + ' / ' + str(self.list_widget_images.count()))

    def open_file_names_dialog(self, mode):
        options = QFileDialog.Options()
        options |= QFileDialog.DontUseNativeDialog
        if mode == 'images':

            files, _ = QFileDialog.getOpenFileNames(None, "choose images", "",
                                                    "Images (*.png *.xpm *.jpg)", options=options)
            if files:
                print(files)

                # copy files to the project label folder
                for file in files:
                    shutil.copy2(file, self.label_dest)

                self.list_widget_images_update()
        elif mode == 'models':

            files, _ = QFileDialog.getOpenFileNames(None, "choose models", "",
                                                    "Models (*.h5)", options=options)
            if files:
                print(files)

                # copy files to the project auto_detect folder
                for file in files:
                    shutil.copy2(file, self.auto_detect_dest)
                self.list_widget_models_update()
        else:
            pass

    def remove_files_handler(self, mode):
        if mode == 'images':
            for item in self.list_widget_images.selectedItems():
                self.list_widget_images.takeItem(self.list_widget_images.row(item))
                os.remove(os.path.join(self.label_dest, item.text()))
            self.list_widget_images_update()
            # self.graphics_view_update()
            self.label_page_id_update()
        elif mode == 'models':
            for item in self.list_widget_models.selectedItems():
                self.list_widget_models.takeItem(self.list_widget_models.row(item))
                os.remove(os.path.join(self.auto_detect_dest, item.text()))
            self.list_widget_models_update()
        else:
            pass

    def selection_handler(self, mode):

        # items = [item for item in self.list_widget_images.selectedItems()]
        # if items is not None:
        #     self.list_widget_images.setCurrentItem(items[0])
        if mode == 'images':
            self.label_page_id_update()
            self.graphics_view_update()
        elif mode == 'models':
            pass
        else:
            pass

    def zoom_handler(self, mode):
        # TODO add wheel event, rewrite the graphic view class using inheritance
        # TODO default size
        if mode == 'zoom_in':
            self.graphics_view.scale(1.1, 1.1)
        elif mode == 'zoom_out':
            self.graphics_view.scale(1 / 1.1, 1 / 1.1)
        # elif mode == 'default_size':
        #     self.graphics_view.scale(1 / 1.1, 1 / 1.1)
        else:
            pass

    def page_turning_handler(self, mode):
        if mode == 'previous_page' and 0 < self.list_widget_images.currentRow() <= self.list_widget_images.count() - 1:

            self.list_widget_images.setCurrentRow(self.list_widget_images.currentRow() - 1)
        elif mode == 'next_page' and 0 <= self.list_widget_images.currentRow() < self.list_widget_images.count() - 1:
            self.list_widget_images.setCurrentRow(self.list_widget_images.currentRow() + 1)
        else:
            pass
        # self.label_page_id_update()

    def go_handler(self):
        item = self.list_widget_models.currentItem()

        # auto.auto_detection(item.text())
        print('done')

    def delete_polygon_handler(self):
        items = self.graphics_view.scene().selectedItems()
        for item in items:
            self.graphics_view.scene().removeItem(item)

    def json2polygons(self, json_data, filename):

        # Load images and add them to the dataset
        polygons = []
        for data in json_data:

            if data["filename"] == filename:
                regions = data['regions']

                for region in regions:
                    points = []
                    num = len(region["shape_attributes"]["all_points_x"])
                    for i in range(0, num):
                        points.append(QPoint(region["shape_attributes"]["all_points_x"][i],
                                             region["shape_attributes"]["all_points_y"][i]))
                    polygons.append(QPolygonF(points))
        return polygons

    def add_attribute_id(self):
        radio_button_group = QButtonGroup(self.groupBox_2)

        radioButton = QRadioButton(self.groupBox_2)
        radioButton.setObjectName("radioButton")
        self.verticalLayout_6.addWidget(radioButton)
        radioButton.setText(self.line_edit_id.text())
        radio_button_group.addButton(radioButton)
    def remove_attribute_id(self):
        if self.radioButton.isChecked():
            self.verticalLayout_6.removeWidget(self.radioButton)




if __name__ == "__main__":
    import sys

    app = QtWidgets.QApplication(sys.argv)
    application = MainSenseController()
    application.show()
    sys.exit(app.exec_())
