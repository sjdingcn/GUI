import os
import threading
from pathlib import Path

from PyQt5 import QtWidgets
from PyQt5.QtWidgets import QDialog, QFileDialog, QMessageBox

from src.view.create_project_scene import Ui_Dialog


class CreateProjectDialog(QDialog, Ui_Dialog):
    def __init__(self):
        super(CreateProjectDialog, self).__init__()
        self.setupUi(self)
        self.line_edit_location.setText('/path/to/untitled/')
        # self.tool_button_location.triggered.connect(self.project_location_handler)
        self.tool_button_location.clicked.connect(self.project_location_handler)

    def project_location_handler(self):
        file = str(QFileDialog.getExistingDirectory(self, "Select Base Directory"))
        self.line_edit_location.setText(file)
        self.accepted.connect(self.project_accept_handler)

    def project_accept_handler(self):

        try:
            Path(self.line_edit_location.text()).mkdir(parents=True, exist_ok=False)

        except FileExistsError:
            # TODO should not close the dialog after press the 'OK' button
            msg = QMessageBox(self)
            msg.setIcon(QMessageBox.Warning)

            msg.setText("The directory is already existed. Please rename.")
            # msg.setInformativeText("This is additional information")
            msg.setWindowTitle("Warning")

            msg.setStandardButtons(QMessageBox.Ok)

            msg.exec_()
            return

        from src.view.main_scene_controller import MainSense

        application = MainSense()
        application.project_dict = self.line_edit_location.text()

        Path(os.path.join(application.project_dict), 'label').mkdir(parents=True, exist_ok=True)
        Path(os.path.join(application.project_dict), 'data').mkdir(parents=True, exist_ok=True)
        Path(os.path.join(application.project_dict), 'data', 'train').mkdir(parents=True, exist_ok=True)
        Path(os.path.join(application.project_dict), 'data', 'val').mkdir(parents=True, exist_ok=True)
        Path(os.path.join(application.project_dict), 'data', 'test').mkdir(parents=True, exist_ok=True)
        Path(os.path.join(application.project_dict), 'logs').mkdir(parents=True, exist_ok=True)
