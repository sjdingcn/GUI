from PyQt5.QtWidgets import QFileDialog
from src.view.appSenseController import *


def open_file_names_dialog():
    options = QFileDialog.Options()
    options |= QFileDialog.DontUseNativeDialog
    files, _ = QFileDialog.getOpenFileNames(None, "choose images", "",
                                            "Images (*.png *.xpm *.jpg)", options=options)
    if files:
        print(files)


class LabelController(Ui_modelMainWindow):
    def set_up_ui2(self, model_main_window):
        self.pushButton.clicked.connect(open_file_names_dialog)
