from PyQt5.QtWidgets import QFileDialog

from src.view.appSenseController import Ui_modelMainWindow


class test(Ui_modelMainWindow):
    def setupUi3(self, modelMainWindow):
        self.pushButton_2.clicked.connect(self.openFileNamesDialog)

    def openFileNamesDialog(self):
        options = QFileDialog.Options()
        options |= QFileDialog.DontUseNativeDialog
        files, _ = QFileDialog.getOpenFileNames(None, "choose images", "",
                                                "Images (*.png *.xpm *.jpg)", options=options)
        if files:
            print(files)
