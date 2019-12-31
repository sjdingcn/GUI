from PyQt5.QtWidgets import QFileDialog
from src.view.modelSenseController import *

class laborController(Ui_modelMainWindow):
    def setupUi2(self, modelMainWindow):
        self.pushButton.clicked.connect(self.openFileNamesDialog)


    def openFileNamesDialog(self):
        options = QFileDialog.Options()
        options |= QFileDialog.DontUseNativeDialog
        files, _ = QFileDialog.getOpenFileNames(None, "choose images", "",
                                                "Images (*.png *.xpm *.jpg)", options=options)
        if files:
            print(files)

if __name__ == "__main__":
    import sys

    app = QtWidgets.QApplication(sys.argv)
    modelMainWindow = QtWidgets.QMainWindow()
    ui = laborController()
    ui.setupUi(modelMainWindow)
    ui.setupUi2(modelMainWindow)
    modelMainWindow.show()
    sys.exit(app.exec_())
