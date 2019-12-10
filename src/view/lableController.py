from PyQt5.QtWidgets import QFileDialog

from src.view.modelSenseController import *


class LabelController(Ui_modelMainWindow):

    def setupUi(self, modelMainWindow):
        self.pushButton.clicked.connect(self.openFileNamesDialog)

    def openFileNamesDialog(self):
        options = QFileDialog.Options()
        options |= QFileDialog.DontUseNativeDialog
        files, _ = QFileDialog.getOpenFileNames(None, "choose images", "",
                                                "Images (*.png *.xpm *.jpg)", options=options)
        if files:
            print(files)