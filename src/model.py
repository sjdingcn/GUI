import os
# import sys
#
# from PyQt5 import uic
# from PyQt5.QtWidgets import QApplication, QWidget
# from PyQt5.QtWebEngineWidgets import QWebEngineView as QWebView,QWebEnginePage as QWebPage
# from PyQt5.QtWebEngineWidgets import QWebEngineSettings as QWebSettings
#
#
#
#
# if __name__ == '__main__':
#     app = QApplication(sys.argv)
#     ui_path = os.path.dirname(os.path.abspath(__file__))
#     Form, Window = uic.loadUi(os.path.join(ui_path, "view/model.ui"))
#     Window.show()
#
#     sys.exit(app.exec_())

from PyQt5 import QtWidgets, uic

import sys

app = QtWidgets.QApplication([])
ui_path = os.path.dirname(os.path.abspath(__file__))
# Form, Window = uic.loadUi(os.path.join(ui_path, "view/model.ui"))
win = uic.loadUi(os.path.join(ui_path, "view/model.ui")) # specify the location of your .ui file

win.show()

sys.exit(app.exec())