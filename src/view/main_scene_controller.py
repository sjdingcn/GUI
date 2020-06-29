import collections
import json
# TODO: replace os with pathlib
import os
import shutil
from pathlib import Path

from PyQt5.QtCore import Qt, QPoint, QSettings
# import sip
from PyQt5.QtGui import QPixmap, QImage, QPen, QPolygonF
from PyQt5.QtWidgets import QFileDialog, QMainWindow, QGraphicsScene, QGraphicsItem, \
    QGraphicsPolygonItem, QGraphicsPixmapItem, QButtonGroup, QRadioButton, QMessageBox

from src.model.ready import Ready
from src.view.create_project_scene_controller import CreateProjectDialog
from src.view.main_scene import *

# from mrcnn import model
from src.view.utils import gui_root


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


class GUIPolygonItem(QGraphicsPolygonItem):
    def __init__(self, polygon, parent):
        super(GUIPolygonItem, self).__init__(polygon, parent)

        # self.setAcceptDrops(True)
        self.id = ''

    def keyPressEvent(self, event):
        if event.key() == Qt.Key_D:
            self.scene().removeItem(self)
            print('delete')

    def mousePressEvent(self, event):
        print(self.id)
        # TODO 'application' need to be optimized
        for button in application.radio_button_group.buttons():
            if self.id == button.text():
                button.setChecked(True)
                print('test')

    # TODO need to be optimized
    # def dragLeaveEvent(self, event):
    #     event.accept()
    #     print('test')
    # polygon_item = GUIPolygonItem(self.poly)
    # polygon_item.setPen(QPen(Qt.yellow, 1, Qt.SolidLine))
    # self.scene().addItem(polygon_item)

    # polygon_item.setFlags(QGraphicsItem.ItemIsMovable | QGraphicsItem.ItemIsSelectable
    #                       | QGraphicsItem.ItemIsFocusable)


class GUIPixmapItem(QGraphicsPixmapItem):
    def __init__(self, pixmap):
        super(GUIPixmapItem, self).__init__(pixmap)
        self.points = []
        self.drawing = False
        # self.start = False
        self.setAcceptHoverEvents(True)

    def mouseDoubleClickEvent(self, event):
        self.drawing = True
        # self.start = True
        self.points.append(event.scenePos())

    def mousePressEvent(self, event):
        # self.start = False

        if self.drawing:
            if event.button() == Qt.LeftButton:
                self.points.append(event.scenePos())
                self.update()
                print(event.scenePos().x())
            elif event.button() == Qt.RightButton:

                polygon_item = GUIPolygonItem(QPolygonF(self.points), self)
                polygon_item.setPen(QPen(Qt.yellow, 1, Qt.SolidLine))
                # self.scene().addItem(polygon_item)

                polygon_item.setFlags(QGraphicsItem.ItemIsMovable | QGraphicsItem.ItemIsSelectable
                                      | QGraphicsItem.ItemIsFocusable)
                # self.scene().update()
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

    # TODO optimize the code: application
    def wheelEvent(self, event):
        if event.modifiers() == QtCore.Qt.ControlModifier:
            if event.delta() == 120:
                MainScene.zoom_handler(application, 'zoom_in')

            elif event.delta() == -120:
                MainScene.zoom_handler(application, 'zoom_out')

            else:
                pass


def json2polygons_ids(json_value, filename):
    # Load images and add them to the dataset
    polygons_ids = []

    for value in json_value:

        if value["filename"] == filename:
            regions = value['regions']

            for region in regions:
                polygon_id = collections.namedtuple('polygon_id', ['polygon', 'id'])
                points = []
                # num = len(region["shape_attributes"]["all_points_x"])
                # for i in range(0, num):
                #     points.append(QPoint(region["shape_attributes"]["all_points_x"][i],
                #                          region["shape_attributes"]["all_points_y"][i]))
                for x, y in zip(region["shape_attributes"]["all_points_x"], region["shape_attributes"]["all_points_y"]):
                    points.append(QPoint(x, y))
                polygon_id.polygon = QPolygonF(points)
                polygon_id.id = region["region_attributes"]["Attribute"]
                polygons_ids.append(polygon_id)

    return polygons_ids


class MainScene(QMainWindow, Ui_MainWindow):
    # projects_dest = '/home/sijie/Desktop/GUI/stock/projects'
    # project_name = 'test'
    # project_dir = os.path.join(projects_dest, project_name)
    #
    # label_dir = os.path.join(project_dir, 'label')
    # model_dir = os.path.join(project_dir, 'auto_detect')
    #
    # print(project_dir)
    # print(label_dir)

    def __init__(self, project_dir, model_dir):
        super(MainScene, self).__init__()

        # self.id = []
        self.project_dir = project_dir

        self.label_dir = os.path.join(self.project_dir, 'label')
        print(self.project_dir)
        print(self.label_dir)
        # TODO optimize model folder
        self.model_dir = model_dir

        self.json_data = {}
        self.setupUi(self)
        try:
            self.readSettings()
            self.list_widget_images_update()
            self.list_widget_models_update()
            self.label_page_id_update()
            self.graphics_view_update()
        except:
            pass

        # Controller for menu bar
        self.action_project_new.triggered.connect(self.project_new_handler)
        self.action_project_open.triggered.connect(self.project_open_handler)
        self.action_project_save.triggered.connect(self.project_save_handler)
        self.action_project_add_images.triggered.connect(lambda: self.open_file_names_dialog('images'))
        self.action_project_remove_images.triggered.connect(lambda: self.remove_files_handler('images'))
        self.action_file_zoom_in.triggered.connect(lambda: self.zoom_handler('zoom_in'))
        self.action_file_zoom_out.triggered.connect(lambda: self.zoom_handler('zoom_out'))
        self.action_file_default_size.triggered.connect(lambda: self.zoom_handler('default_size'))
        self.action_file_delete_polygon.triggered.connect(self.delete_polygon_handler)
        self.action_train_edit_configurations.triggered.connect(self.train_configurations_handler)
        self.action_train_train.triggered.connect(self.train_handler)
        self.action_analyze_tensorboard.triggered.connect(self.analyze_tensorboard_handler)

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
        if self.graphics_view.scene():
            self.graphics_view.scene().changed.connect(self.polygons_ids2json)

        # controller for manually tab
        self.radio_button_group = QButtonGroup(self.groupBox_2)
        self.radio_button_group.setExclusive(True)
        self.push_button_add.clicked.connect(self.add_attribute_id)
        self.push_button_remove.clicked.connect(self.remove_attribute_id)
        self.radio_button_group.buttonClicked.connect(self.id_changed_handler)
        print(self.radio_button_group.buttons())
        for button in self.radio_button_group.buttons():
            self.verticalLayout_6.addWidget(button)
        # self.graphics_view.scene().selectionChanged.connect(self.clear_all_check)

    # def clear_all_check(self):
    #     for button in self.radio_button_group.buttons():
    #         button.setChecked(False)
    #         print(self.radio_button_group.buttons())
    #     print('clear')

    def closeEvent(self, event):
        settings = QSettings("HSG", "GUI")
        settings.setValue("geometry", self.saveGeometry())
        settings.setValue("windowState", self.saveState())
        # TODO in welcome try to open the address in json, if fail then pop up the welcome sense
        with open(Path(gui_root() / 'stock', 'gui.json'), 'w') as outfile:
            json.dump(str(self.project_dir), outfile)
        QMainWindow.closeEvent(self, event)
        print('close')

    # TODO unfinished
    def readSettings(self):
        settings = QSettings("HSG", "GUI")
        self.restoreGeometry(settings.value("geometry"))
        self.restoreState(settings.value("windowState"))

    def project_new_handler(self):

        create_project_dialog = CreateProjectDialog()
        create_project_dialog.exec()

    def project_open_handler(self):
        # TODO open existed project
        return

    def project_save_handler(self):
        # TODO do not overwrite the json file each time, in case not every image was labeled (sometimes it may success?)
        with open(os.path.join(self.label_dir, 'data.json'), 'w') as outfile:
            json.dump(self.json_data, outfile)
        # print('test')

    def list_widget_images_update(self):

        self.list_widget_images.clear()
        self.list_widget_images.addItems(get_files_from_dir(self.label_dir, 'images'))
        self.list_widget_images.setCurrentRow(0)

    def list_widget_models_update(self):

        self.list_widget_models.clear()
        self.list_widget_models.addItems(get_files_from_dir(self.model_dir, 'models'))
        self.list_widget_models.setCurrentRow(0)

    def graphics_view_update(self):

        scene = QGraphicsScene(self.graphics_view)

        item = self.list_widget_images.currentItem()

        if item is not None:
            image_name = os.path.join(self.label_dir, item.text())
            scene.clear()
            with open(image_name, 'rb') as f:
                img = f.read()
            image = QImage.fromData(img)
            pix_map = QPixmap.fromImage(image)
            pixmap_item = GUIPixmapItem(pix_map)
            # pixmap_item.setPixmap(pix_map)
            scene.addItem(pixmap_item)

            # Read dataset information from the json file
            try:
                self.json_data = json.load(open(os.path.join(self.label_dir, "data.json")))
            except FileNotFoundError:
                pass

            # Transfer dict to list
            json_value = list(self.json_data.values())
            polygons_ids = json2polygons_ids(json_value, item.text())

            for polygon_id in polygons_ids:
                polygon_item = GUIPolygonItem(polygon_id.polygon, pixmap_item)
                polygon_item.setPen(QPen(Qt.yellow, 1, Qt.SolidLine))
                # scene.addItem(polygon_item)

                polygon_item.setFlags(QGraphicsItem.ItemIsMovable | QGraphicsItem.ItemIsSelectable
                                      | QGraphicsItem.ItemIsFocusable)
                polygon_item.id = polygon_id.id

            print('polygons')
        else:
            scene.clear()
        # scene.update()

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
                    shutil.copy2(file, self.label_dir)

                self.list_widget_images_update()
        elif mode == 'models':

            files, _ = QFileDialog.getOpenFileNames(None, "choose models", "",
                                                    "Models (*.h5)", options=options)
            if files:
                print(files)

                # copy files to the project auto_detect folder
                for file in files:
                    shutil.copy2(file, self.model_dir)
                self.list_widget_models_update()
        else:
            pass

    def remove_files_handler(self, mode):
        if mode == 'images':
            for item in self.list_widget_images.selectedItems():
                self.list_widget_images.takeItem(self.list_widget_images.row(item))
                os.remove(os.path.join(self.label_dir, item.text()))
            self.list_widget_images_update()
            # self.graphics_view_update()
            self.label_page_id_update()
        elif mode == 'models':
            for item in self.list_widget_models.selectedItems():
                self.list_widget_models.takeItem(self.list_widget_models.row(item))
                os.remove(os.path.join(self.model_dir, item.text()))
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
        from src.model.auto_detect import Auto
        item = self.list_widget_models.currentItem()

        Auto(self.project_dir, self.model_dir, item.text()).detect()

        # self.json_data.clear()
        self.graphics_view_update()
        print('done')

    def delete_polygon_handler(self):
        items = self.graphics_view.scene().selectedItems()
        for item in items:
            self.graphics_view.scene().removeItem(item)

    def add_attribute_id(self):

        radio_button = QRadioButton(self.groupBox_2)
        radio_button.setObjectName("radio_button")
        self.verticalLayout_6.addWidget(radio_button)
        radio_button.setText(self.line_edit_id.text())
        self.radio_button_group.addButton(radio_button)
        # self.id.append(radio_button.text())

    def remove_attribute_id(self):
        self.verticalLayout_6.removeWidget(self.radio_button_group.checkedButton())
        self.radio_button_group.checkedButton().deleteLater()
        self.radio_button_group.removeButton(self.radio_button_group.checkedButton())
        # self.id.remove(self.radio_button_group.checkedButton().text())

    def polygons_ids2json(self):
        # self.graphics_view.scene().update()
        regions = []
        for item in self.graphics_view.scene().items():
            if isinstance(item, GUIPolygonItem):
                # print(item.pos())
                ##########################
                x = []
                y = []
                for i in range(0, item.polygon().count()):
                    x.append(item.polygon().toPolygon().point(i).x() + item.pos().x())
                    y.append(item.polygon().toPolygon().point(i).y() + item.pos().y())
                ################################
                # print(x)
                # print(y)
                # item.setPos(item.pos())
                # x1 = []
                # y1 = []
                # for i in range(0, item.polygon().count()):
                #     # item.setPos(item.pos())
                #     x1.append(item.polygon().toPolygon().point(i).x())
                #     y1.append(item.polygon().toPolygon().point(i).y())
                # print(x1)
                # print(y1)

                region = {"shape_attributes": {"name": "polygon", "all_points_x": x,
                                               "all_points_y": y},
                          "region_attributes": {"Attribute": item.id}}
                # print(item.id)
                regions.append(region)
        if self.list_widget_images.currentItem():
            filename = self.list_widget_images.currentItem().text()
            path = os.path.join(self.label_dir, filename)

            size = os.stat(path).st_size
            key = filename + str(size)

            self.json_data[key] = {"filename": filename, "size": size, "regions": regions, "file_attributes": {}}
            self.project_save_handler()

    def id_changed_handler(self):
        if self.graphics_view.scene().selectedItems() and self.radio_button_group.checkedButton():
            self.graphics_view.scene().selectedItems()[0].id = self.radio_button_group.checkedButton().text()
        self.polygons_ids2json()
        print('tetsstest')

    def train_configurations_handler(self):
        train_config = Ready(self.project_dir)
        train_config.image_rotate()
        train_config.json_rotate()
        msg = QMessageBox()
        msg.setIcon(QMessageBox.Information)

        msg.setText("Edit Training Configurations Successfully")
        # msg.setInformativeText("This is additional information")
        msg.setWindowTitle("Ready to Train")

        msg.setStandardButtons(QMessageBox.Ok)
        msg.exec_()

    def train_handler(self):
        # TODO
        # shut after end of running
        # os.system("gnome-terminal -e 'python3 /home/sijie/Desktop/GUI/src/model/project.py train "
        #           "--dataset=/home/sijie/Desktop/GUI/stock/projects/test/data --weights=coco'")
        # not shut after end of running
        # os.path.join(self.project_dir, 'data')
        os.system("gnome-terminal -e 'bash -c \"python3 " + str(gui_root() / 'src' / 'model' / 'project.py') + " train "
                                                                                                               "--dataset=" + str(
            self.project_dir / 'data') + " --weights=coco; exec bash\"'")

    def analyze_tensorboard_handler(self):
        # TODO
        # os.path.join(self.project_dir, 'logs')
        weights_path = '/home/sijie/Desktop/Sijie/ALCUBrass/logs/alcubrass20191018T1524/'
        # weights_path = max(glob.glob(os.path.join('/home/sijie/Desktop/GUI/stock/projects/test/logs/', '*/')), key=os.path.getmtime)
        os.system(
            "gnome-terminal -e 'bash -c \"tensorboard --logdir " + str(self.project_dir / 'logs') + "; exec bash\"'")


if __name__ == "__main__":
    import sys

    app = QtWidgets.QApplication(sys.argv)
    application = MainScene(Path('/home/gemc/Desktop/GUItest/project'), Path('/home/gemc/Desktop/GUI/stock'))
    application.show()
    sys.exit(app.exec_())
