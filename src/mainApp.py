# from src.view.modelSenseController import *
from src.view.labelController import *

from PyQt5 import uic, QtWidgets

from src.view.trainController import test


class mainApp(laborController, test):
    pass

if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    modelMainWindow = QtWidgets.QMainWindow()
    ui = mainApp()
    ui.setupUi(modelMainWindow)
    ui.setupUi2(modelMainWindow)
    ui.setupUi3(modelMainWindow)
    modelMainWindow.show()
    sys.exit(app.exec_())