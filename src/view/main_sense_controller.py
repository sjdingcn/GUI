from PyQt5.QtWidgets import QFileDialog, QMainWindow
from src.view.main_sense import *


def open_file_names_dialog():
    options = QFileDialog.Options()
    options |= QFileDialog.DontUseNativeDialog
    files, _ = QFileDialog.getOpenFileNames(None, "choose images", "",
                                            "Images (*.png *.xpm *.jpg)", options=options)
    if files:
        print(files)


class MainSenseController(QMainWindow, Ui_MainWindow):
    def __init__(self):
        super(MainSenseController, self).__init__()

        self.setupUi(self)

        self.action_project_add_files.triggered.connect(open_file_names_dialog)
        self.action_project_add_files.triggered.connect(open_file_names_dialog)

if __name__ == "__main__":
    import sys

    app = QtWidgets.QApplication(sys.argv)
    application = MainSenseController()
    application.show()
    sys.exit(app.exec_())
