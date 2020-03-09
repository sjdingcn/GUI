import os
import threading
import time
from pathlib import Path

from PyQt5 import QtWidgets
from PyQt5.QtWidgets import QDialog, QFileDialog, QMessageBox, QDialogButtonBox

from src.view.welcome_scene import Ui_Dialog
from src.view.create_project_scene_controller import CreateProjectDialog


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
        # TODO unfinished
        file = str(QFileDialog.getExistingDirectory(self, "Open Project"))
        # self.done(0)
        return


if __name__ == "__main__":
    import sys

    app = QtWidgets.QApplication(sys.argv)
    application = WelcomeDialog()
    application.show()
    sys.exit(app.exec_())
