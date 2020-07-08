import collections
import json
import os
import shutil
import subprocess
from pathlib import Path

from PyQt5.QtCore import Qt, QPoint, QSettings, pyqtSlot
from PyQt5.QtGui import QPixmap, QImage, QPen, QPolygonF
from PyQt5.QtWidgets import QFileDialog, QMainWindow, QGraphicsScene, QGraphicsItem, QGraphicsPolygonItem, \
    QGraphicsPixmapItem, QButtonGroup, QRadioButton, QMessageBox, QGraphicsView, QAbstractButton

from src.view.create_project_scene_controller import CreateProjectDialog
from src.view.main_scene import *
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
        self.id = ''

    def keyPressEvent(self, event):
        if event.key() == Qt.Key_D:
            self.scene().removeItem(self)
            print('delete')


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

    def __init__(self, project_dir, model_dir):
        super(MainScene, self).__init__()

        # self.id = []
        self.project_dir = project_dir

        self.label_dir = Path(self.project_dir, 'label')
        print(self.project_dir)
        print(self.label_dir)
        self.model_dir = model_dir
        self.json_data = {}
        self.setupUi(self)
        self.graphics_view.setTransformationAnchor(QGraphicsView.AnchorUnderMouse)
        # self.graphics_view.setDragMode(QGraphicsView.ScrollHandDrag)
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
        self.project_name.setText(str(self.project_dir))
        self.list_widget_images.itemSelectionChanged.connect(lambda: self.selection_handler('images'))
        self.push_button_add_images.clicked.connect(lambda: self.open_file_names_dialog('images'))
        self.push_button_remove_images.clicked.connect(lambda: self.remove_files_handler('images'))

        # Controller for list widget of models
        self.list_widget_models.itemSelectionChanged.connect(lambda: self.selection_handler('models'))
        self.push_button_add_models.clicked.connect(lambda: self.open_file_names_dialog('models'))
        self.push_button_remove_models.clicked.connect(lambda: self.remove_files_handler('models'))
        self.push_button_go.clicked.connect(self.go_handler)

        # self.pushButton.pressed.connect(self.handleButton)

        # Controller for graphic view
        self.button_previous_page.clicked.connect(lambda: self.page_turning_handler('previous_page'))
        self.button_next_page.clicked.connect(lambda: self.page_turning_handler('next_page'))
        if self.graphics_view.scene():
            self.graphics_view.scene().selectionChanged.connect(self.polygon_id2radio_checked)
            self.graphics_view.scene().changed.connect(self.polygons_ids2json)

        # controller for manually tab
        self.radio_button_group = QButtonGroup(self.groupBox_2)
        self.radio_button_group.setExclusive(False)
        self.push_button_add.clicked.connect(self.add_attribute_id)
        self.push_button_remove.clicked.connect(self.remove_attribute_id)
        # self.radio_button_group.buttonClicked.connect(self.id_changed_handler)
        self.radio_button_group.buttonClicked[QAbstractButton].connect(lambda i: self.id_changed_handler(i))
        print(self.radio_button_group.buttons())

        for attribute in json.load(open(Path(self.project_dir, "project.json"))):
            print(attribute)
            radio_button = QRadioButton(self.groupBox_2)
            radio_button.setObjectName("radio_button")
            radio_button.setText(attribute)
            self.radio_button_group.addButton(radio_button)
        for button in self.radio_button_group.buttons():
            self.verticalLayout_6.addWidget(button)

    def clear_all_check(self):
        for button in self.radio_button_group.buttons():
            button.setChecked(False)
            print(self.radio_button_group.buttons())
        print('clear')

    def closeEvent(self, event):
        self.project_save_handler()
        settings = QSettings("HSG", "GUI")
        settings.setValue("geometry", self.saveGeometry())
        settings.setValue("windowState", self.saveState())
        with open(Path(gui_root() / 'stock', 'gui.json'), 'w') as outfile:
            json.dump(str(self.project_dir), outfile)
        QMainWindow.closeEvent(self, event)
        print('close')

    def readSettings(self):
        settings = QSettings("HSG", "GUI")
        self.restoreGeometry(settings.value("geometry"))
        self.restoreState(settings.value("windowState"))

    def project_new_handler(self):

        create_project_dialog = CreateProjectDialog()
        create_project_dialog.exec()

    def project_open_handler(self):
        file = QFileDialog.getExistingDirectory(self, "Open Project")
        print(file)
        if file:
            if Path(file, 'project.json').is_file():
                new_main = MainScene(Path(file), model_dir=gui_root() / 'stock')
                new_main.show()
                self.project_save_handler()
                self.close()
                # self.done(1)
            else:
                msg = QMessageBox(self)
                msg.setIcon(QMessageBox.Warning)

                msg.setText("'" + file + "' is not a project.")
                msg.setInformativeText("Please select an existing project.")
                msg.setWindowTitle("Warning")

                msg.setStandardButtons(QMessageBox.Ok)

                msg.exec_()
        return

    def project_save_handler(self):
        with open(Path(self.label_dir, 'data.json'), 'w') as outfile:
            json.dump(self.json_data, outfile)
        with open(Path(self.project_dir, 'project.json'), 'w') as outfile:
            attributes = [x.text() for x in self.radio_button_group.buttons()]
            json.dump(attributes, outfile)

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
            image_name = Path(self.label_dir, item.text())
            scene.clear()
            with open(image_name, 'rb') as f:
                img = f.read()
            image = QImage.fromData(img)
            pix_map = QPixmap.fromImage(image)
            pixmap_item = GUIPixmapItem(pix_map)
            scene.addItem(pixmap_item)

            # Read dataset information from the json file
            try:
                self.json_data = json.load(open(Path(self.label_dir, "data.json")))
            except FileNotFoundError:
                pass

            # Transfer dict to list
            json_value = list(self.json_data.values())
            polygons_ids = json2polygons_ids(json_value, item.text())

            for polygon_id in polygons_ids:
                polygon_item = GUIPolygonItem(polygon_id.polygon, pixmap_item)
                polygon_item.setPen(QPen(Qt.yellow, 1, Qt.SolidLine))

                polygon_item.setFlags(QGraphicsItem.ItemIsMovable | QGraphicsItem.ItemIsSelectable
                                      | QGraphicsItem.ItemIsFocusable)
                polygon_item.id = polygon_id.id

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
                os.remove(Path(self.label_dir, item.text()))
            self.list_widget_images_update()
            self.label_page_id_update()
        elif mode == 'models':
            for item in self.list_widget_models.selectedItems():
                self.list_widget_models.takeItem(self.list_widget_models.row(item))
                os.remove(Path(self.model_dir, item.text()))
            self.list_widget_models_update()
        else:
            pass

    def selection_handler(self, mode):

        if mode == 'images':
            self.label_page_id_update()
            self.graphics_view_update()
        elif mode == 'models':
            pass
        else:
            pass

    def wheelEvent(self, event):
        if event.modifiers() == QtCore.Qt.ControlModifier:
            if event.angleDelta().y() == 120:
                self.zoom_handler('zoom_in')

            elif event.angleDelta().y() == -120:
                self.zoom_handler('zoom_out')

            else:
                pass

    def zoom_handler(self, mode):
        if mode == 'zoom_in':
            self.graphics_view.scale(1.1, 1.1)
        elif mode == 'zoom_out':
            self.graphics_view.scale(1 / 1.1, 1 / 1.1)
        elif mode == 'default_size':
            self.graphics_view.resetTransform()
        else:
            pass

    def page_turning_handler(self, mode):
        if mode == 'previous_page' and 0 < self.list_widget_images.currentRow() <= self.list_widget_images.count() - 1:

            self.list_widget_images.setCurrentRow(self.list_widget_images.currentRow() - 1)
        elif mode == 'next_page' and 0 <= self.list_widget_images.currentRow() < self.list_widget_images.count() - 1:
            self.list_widget_images.setCurrentRow(self.list_widget_images.currentRow() + 1)
        else:
            pass

    def go_handler(self):
        try:
            self.push_button_go.setDown(True)
            self.statusbar.showMessage('Please wait, processing...')

            from src.model.auto_detect import detect
            item = self.list_widget_models.currentItem()

            detect(self.project_dir, self.model_dir, item.text())
            self.graphics_view_update()
            self.statusbar.showMessage('Done')
            self.push_button_go.setDown(False)
        except:
            self.statusBar.showMessage('ERROR')

    def delete_polygon_handler(self):
        items = self.graphics_view.scene().selectedItems()
        for item in items:
            self.graphics_view.scene().removeItem(item)

    def add_attribute_id(self):

        if self.line_edit_id.text() in [x.text() for x in self.radio_button_group.buttons()]:
            msg = QMessageBox(self)
            msg.setIcon(QMessageBox.Warning)
            msg.setText("Attributes cannot be duplicated.")
            msg.setWindowTitle("Warning")
            msg.setStandardButtons(QMessageBox.Ok)
            msg.exec_()
        else:
            radio_button = QRadioButton(self.groupBox_2)
            radio_button.setObjectName("radio_button")
            self.verticalLayout_6.addWidget(radio_button)
            radio_button.setText(self.line_edit_id.text())
            self.radio_button_group.addButton(radio_button)
        self.line_edit_id.clear()
        self.project_save_handler()

    def remove_attribute_id(self):
        self.verticalLayout_6.removeWidget(self.radio_button_group.checkedButton())
        self.radio_button_group.checkedButton().deleteLater()
        self.radio_button_group.removeButton(self.radio_button_group.checkedButton())
        self.project_save_handler()

    def polygon_id2radio_checked(self):
        self.clear_all_check()
        polygon_id = self.graphics_view.scene().selectedItems()[0].id
        for button in self.radio_button_group.buttons():
            if polygon_id == button.text():
                button.setChecked(True)
                print('test')

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
            path = Path(self.label_dir, filename)

            size = os.stat(path).st_size
            key = filename + str(size)

            self.json_data[key] = {"filename": filename, "size": size, "regions": regions, "file_attributes": {}}
            self.project_save_handler()

    @pyqtSlot(QAbstractButton)
    def id_changed_handler(self, b):

        for button in self.radio_button_group.buttons():
            if button.text == b.text:
                continue
            button.setChecked(False)

        if self.graphics_view.scene().selectedItems() and self.radio_button_group.checkedButton():
            self.graphics_view.scene().selectedItems()[0].id = self.radio_button_group.checkedButton().text()
        self.polygons_ids2json()
        print('tetsstest')

    def train_configurations_handler(self):

        shutil.copyfile(Path(gui_root(), 'src', 'model', 'project.py'), Path(self.project_dir, 'train_config.py'))
        opener = "open" if sys.platform == "darwin" else "xdg-open"
        subprocess.call([opener, Path(self.project_dir, 'train_config.py')])

        # train_config = Ready(self.project_dir)
        # train_config.image_rotate()
        # train_config.json_rotate()
        # msg = QMessageBox()
        # msg.setIcon(QMessageBox.Information)
        #
        # msg.setText("Edit Training Configurations Successfully")
        # # msg.setInformativeText("This is additional information")
        # msg.setWindowTitle("Ready to Train")
        #
        # msg.setStandardButtons(QMessageBox.Ok)
        # msg.exec_()

    def train_handler(self):

        attributes = [x.text() for x in self.radio_button_group.buttons()]

        print(','.join(map(str, attributes)))
        os.system("gnome-terminal -e 'bash -c \"python3 " + str(Path(self.project_dir, 'train_config.py'))
                  + " --dataset=" + str(Path(self.project_dir, 'data')) + " --logs="
                  + str(Path(self.project_dir, 'logs')) + " --attributes=" + ','.join(
            map(str, attributes)) + "; exec bash\"'")

    def analyze_tensorboard_handler(self):

        os.system(
            "gnome-terminal -e 'bash -c \"tensorboard --logdir " + str(
                Path(self.project_dir, 'logs')) + "; exec bash\"'")


if __name__ == "__main__":
    import sys

    app = QtWidgets.QApplication(sys.argv)
    application = MainScene(Path('/home/sijie/Desktop/test_project'), Path('/home/sijie/Desktop/GUI/stock'))
    application.show()
    sys.exit(app.exec_())
