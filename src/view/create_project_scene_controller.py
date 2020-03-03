import os
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

    # def done(self, a0: int):
    # TODO set parent

    def accept(self):
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

            from src.view.main_scene_controller import MainSense

            application = MainSense(self.line_edit_location.text())
            application.show()

            Path(os.path.join(application.project_dict), 'label').mkdir(parents=True, exist_ok=True)
            Path(os.path.join(application.project_dict), 'data').mkdir(parents=True, exist_ok=True)
            Path(os.path.join(application.project_dict), 'data', 'train').mkdir(parents=True, exist_ok=True)
            Path(os.path.join(application.project_dict), 'data', 'val').mkdir(parents=True, exist_ok=True)
            Path(os.path.join(application.project_dict), 'data', 'test').mkdir(parents=True, exist_ok=True)
            Path(os.path.join(application.project_dict), 'logs').mkdir(parents=True, exist_ok=True)

            # close the dialog.
            self.done(0)
