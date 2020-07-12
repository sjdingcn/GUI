import json
from pathlib import Path

from PyQt5 import QtWidgets
from PyQt5.QtWidgets import QDialog, QFileDialog

from create_project_scene_controller import CreateProjectDialog
from main_scene_controller import MainScene
from utils import gui_root, warning_msg_box
from welcome_scene import Ui_Dialog


class WelcomeDialog(QDialog, Ui_Dialog):

    def __init__(self):
        super(WelcomeDialog, self).__init__()
        self.setupUi(self)
        self.push_button_create.clicked.connect(self.create_handler)
        self.push_button_open.clicked.connect(self.open_handler)

    def create_handler(self):
        create_project_dialog = CreateProjectDialog()
        ret = create_project_dialog.exec()
        if ret == QDialog.Accepted:
            self.done(1)
        else:
            pass

    def open_handler(self):
        file = QFileDialog.getExistingDirectory(self, "Open Project")
        if file:
            if Path(file, 'project.json').is_file():
                new_main = MainScene(Path(file), model_dir=gui_root() / 'stock')
                new_main.show()
                self.done(1)
            else:
                warning_msg_box(self, "'" + file + "' is not a project.", "Please select an existing project.")


if __name__ == "__main__":
    import sys

    app = QtWidgets.QApplication(sys.argv)
    try:
        path = json.load(open(Path(gui_root() / 'stock' / 'gui.json')))
        if Path(path, 'project.json').is_file():
            main = MainScene(path, model_dir=gui_root() / 'stock')
            main.show()
        else:
            application = WelcomeDialog()
            application.show()
    except FileNotFoundError:
        application = WelcomeDialog()
        application.show()
    sys.exit(app.exec_())
