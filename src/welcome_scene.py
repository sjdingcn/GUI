# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'welcome_scene.ui'
#
# Created by: PyQt5 UI code generator 5.9.2
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_Dialog(object):
    def setupUi(self, Dialog):
        Dialog.setObjectName("Dialog")
        Dialog.resize(812, 588)
        self.verticalLayout = QtWidgets.QVBoxLayout(Dialog)
        self.verticalLayout.setObjectName("verticalLayout")
        self.horizontalLayout = QtWidgets.QHBoxLayout()
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.verticalLayout_2 = QtWidgets.QVBoxLayout()
        self.verticalLayout_2.setObjectName("verticalLayout_2")
        self.label = QtWidgets.QLabel(Dialog)
        self.label.setText("")
        self.label.setPixmap(QtGui.QPixmap("../icons/quill-drawing-a-line.svg"))
        self.label.setAlignment(QtCore.Qt.AlignCenter)
        self.label.setObjectName("label")
        self.verticalLayout_2.addWidget(self.label)
        self.widget = QtWidgets.QWidget(Dialog)
        self.widget.setObjectName("widget")
        self.verticalLayoutWidget_2 = QtWidgets.QWidget(self.widget)
        self.verticalLayoutWidget_2.setGeometry(QtCore.QRect(320, 20, 161, 171))
        self.verticalLayoutWidget_2.setObjectName("verticalLayoutWidget_2")
        self.verticalLayout_3 = QtWidgets.QVBoxLayout(self.verticalLayoutWidget_2)
        self.verticalLayout_3.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout_3.setObjectName("verticalLayout_3")
        self.push_button_create = QtWidgets.QPushButton(self.verticalLayoutWidget_2)
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap("../icons/add-24px.svg"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.push_button_create.setIcon(icon)
        self.push_button_create.setFlat(True)
        self.push_button_create.setObjectName("push_button_create")
        self.verticalLayout_3.addWidget(self.push_button_create)
        self.push_button_open = QtWidgets.QPushButton(self.verticalLayoutWidget_2)
        icon1 = QtGui.QIcon()
        icon1.addPixmap(QtGui.QPixmap("../icons/folder_open-24px.svg"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.push_button_open.setIcon(icon1)
        self.push_button_open.setDefault(False)
        self.push_button_open.setFlat(True)
        self.push_button_open.setObjectName("push_button_open")
        self.verticalLayout_3.addWidget(self.push_button_open)
        self.verticalLayout_2.addWidget(self.widget)
        self.horizontalLayout.addLayout(self.verticalLayout_2)
        self.verticalLayout.addLayout(self.horizontalLayout)

        self.retranslateUi(Dialog)
        QtCore.QMetaObject.connectSlotsByName(Dialog)

    def retranslateUi(self, Dialog):
        _translate = QtCore.QCoreApplication.translate
        Dialog.setWindowTitle(_translate("Dialog", "Welcome"))
        self.push_button_create.setText(_translate("Dialog", "Creat New Project"))
        self.push_button_open.setText(_translate("Dialog", "Open"))
