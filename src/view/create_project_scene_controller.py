import os
import json

import threading
import time
from pathlib import Path

from PyQt5 import QtWidgets
from PyQt5.QtWidgets import QDialog, QFileDialog, QMessageBox, QDialogButtonBox

from src.view.create_project_scene import Ui_Dialog


class CreateProjectDialog(QDialog, Ui_Dialog):

    def __init__(self):
        super(CreateProjectDialog, self).__init__()
        self.setupUi(self)
        self.line_edit_location.setText('/path/to/untitled/')
        self.tool_button_location.clicked.connect(self.project_location_handler)

    def project_location_handler(self):
        file = str(QFileDialog.getExistingDirectory(self, "Select Base Directory"))
        self.line_edit_location.setText(file)

    # TODO set parent

    def accept(self):
        try:
            if len(os.listdir(self.line_edit_location.text())) != 0:
                print("Directory is not empty")
                msg = QMessageBox(self)
                msg.setIcon(QMessageBox.Warning)

                msg.setText("The directory is not empty. Please select an empty directory.")
                # msg.setInformativeText("Confirm to continue?")
                msg.setWindowTitle("Warning")

                msg.setStandardButtons(QMessageBox.Ok)

                msg.exec_()

            else:

                Path(self.line_edit_location.text()).mkdir(parents=True, exist_ok=True)

                from src.view.main_scene_controller import MainScene
                model_dir = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(__file__))), 'stock')

                application = MainScene(self.line_edit_location.text(), model_dir)
                application.show()

                Path(application.project_dir, 'label').mkdir(parents=True, exist_ok=True)
                Path(application.project_dir, 'data').mkdir(parents=True, exist_ok=True)
                Path(application.project_dir, 'data', 'train').mkdir(parents=True, exist_ok=True)
                Path(application.project_dir, 'data', 'val').mkdir(parents=True, exist_ok=True)
                Path(application.project_dir, 'data', 'test').mkdir(parents=True, exist_ok=True)
                Path(application.project_dir, 'logs').mkdir(parents=True, exist_ok=True)

                data = {}
                with open(os.path.join(application.project_dir, 'project.json'), 'w') as outfile:
                    json.dump(data, outfile)
                # close the dialog.
                self.done(1)

        except FileNotFoundError:
            print("No such or directory: " + self.line_edit_location.text())
            msg = QMessageBox(self)
            msg.setIcon(QMessageBox.Warning)

            msg.setText("No such or directory: '" + self.line_edit_location.text() + "'")
            msg.setInformativeText("Please select an existing directory.")
            msg.setWindowTitle("Warning")

            msg.setStandardButtons(QMessageBox.Ok)

            msg.exec_()



