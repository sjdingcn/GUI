from src.view.modelSenseController import Ui_modelMainWindow
from PyQt5 import uic, QtWidgets


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    modelMainWindow = QtWidgets.QMainWindow()
    ui = Ui_modelMainWindow()
    ui.setupUi(modelMainWindow)
    modelMainWindow.show()
    sys.exit(app.exec_())