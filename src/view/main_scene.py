# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'main_scene.ui'
#
# Created by: PyQt5 UI code generator 5.9.2
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(1145, 818)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(MainWindow.sizePolicy().hasHeightForWidth())
        MainWindow.setSizePolicy(sizePolicy)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.horizontalLayout_4 = QtWidgets.QHBoxLayout(self.centralwidget)
        self.horizontalLayout_4.setObjectName("horizontalLayout_4")
        self.verticalLayout_3 = QtWidgets.QVBoxLayout()
        self.verticalLayout_3.setSizeConstraint(QtWidgets.QLayout.SetDefaultConstraint)
        self.verticalLayout_3.setObjectName("verticalLayout_3")
        self.verticalLayout_4 = QtWidgets.QVBoxLayout()
        self.verticalLayout_4.setObjectName("verticalLayout_4")
        self.formLayout = QtWidgets.QFormLayout()
        self.formLayout.setSizeConstraint(QtWidgets.QLayout.SetDefaultConstraint)
        self.formLayout.setFieldGrowthPolicy(QtWidgets.QFormLayout.AllNonFixedFieldsGrow)
        self.formLayout.setRowWrapPolicy(QtWidgets.QFormLayout.DontWrapRows)
        self.formLayout.setFormAlignment(QtCore.Qt.AlignLeading|QtCore.Qt.AlignLeft|QtCore.Qt.AlignTop)
        self.formLayout.setSpacing(6)
        self.formLayout.setObjectName("formLayout")
        self.sdfLabel = QtWidgets.QLabel(self.centralwidget)
        self.sdfLabel.setObjectName("sdfLabel")
        self.formLayout.setWidget(0, QtWidgets.QFormLayout.LabelRole, self.sdfLabel)
        self.project_name = QtWidgets.QLabel(self.centralwidget)
        self.project_name.setObjectName("project_name")
        self.formLayout.setWidget(0, QtWidgets.QFormLayout.FieldRole, self.project_name)
        self.verticalLayout_4.addLayout(self.formLayout)
        self.list_widget_images = QtWidgets.QListWidget(self.centralwidget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.MinimumExpanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.list_widget_images.sizePolicy().hasHeightForWidth())
        self.list_widget_images.setSizePolicy(sizePolicy)
        self.list_widget_images.setSelectionMode(QtWidgets.QAbstractItemView.ExtendedSelection)
        self.list_widget_images.setObjectName("list_widget_images")
        self.verticalLayout_4.addWidget(self.list_widget_images)
        self.horizontalLayout_2 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_2.setObjectName("horizontalLayout_2")
        self.push_button_add_images = QtWidgets.QPushButton(self.centralwidget)
        self.push_button_add_images.setObjectName("push_button_add_images")
        self.horizontalLayout_2.addWidget(self.push_button_add_images)
        self.push_button_remove_images = QtWidgets.QPushButton(self.centralwidget)
        self.push_button_remove_images.setObjectName("push_button_remove_images")
        self.horizontalLayout_2.addWidget(self.push_button_remove_images)
        self.verticalLayout_4.addLayout(self.horizontalLayout_2)
        self.line_2 = QtWidgets.QFrame(self.centralwidget)
        self.line_2.setFrameShape(QtWidgets.QFrame.HLine)
        self.line_2.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.line_2.setObjectName("line_2")
        self.verticalLayout_4.addWidget(self.line_2)
        self.tabWidget_2 = QtWidgets.QTabWidget(self.centralwidget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.tabWidget_2.sizePolicy().hasHeightForWidth())
        self.tabWidget_2.setSizePolicy(sizePolicy)
        self.tabWidget_2.setMinimumSize(QtCore.QSize(0, 0))
        self.tabWidget_2.setMaximumSize(QtCore.QSize(282, 16777215))
        self.tabWidget_2.setObjectName("tabWidget_2")
        self.tabWidget_2Page1 = QtWidgets.QWidget()
        self.tabWidget_2Page1.setObjectName("tabWidget_2Page1")
        self.verticalLayout = QtWidgets.QVBoxLayout(self.tabWidget_2Page1)
        self.verticalLayout.setObjectName("verticalLayout")
        self.verticalLayout_5 = QtWidgets.QVBoxLayout()
        self.verticalLayout_5.setObjectName("verticalLayout_5")
        self.horizontalLayout_6 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_6.setObjectName("horizontalLayout_6")
        self.label = QtWidgets.QLabel(self.tabWidget_2Page1)
        self.label.setObjectName("label")
        self.horizontalLayout_6.addWidget(self.label)
        self.push_button_add_models = QtWidgets.QPushButton(self.tabWidget_2Page1)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.push_button_add_models.sizePolicy().hasHeightForWidth())
        self.push_button_add_models.setSizePolicy(sizePolicy)
        self.push_button_add_models.setText("")
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap("../../icons/add_circle_outline-24px.svg"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.push_button_add_models.setIcon(icon)
        self.push_button_add_models.setIconSize(QtCore.QSize(18, 18))
        self.push_button_add_models.setObjectName("push_button_add_models")
        self.horizontalLayout_6.addWidget(self.push_button_add_models)
        self.push_button_remove_models = QtWidgets.QPushButton(self.tabWidget_2Page1)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.push_button_remove_models.sizePolicy().hasHeightForWidth())
        self.push_button_remove_models.setSizePolicy(sizePolicy)
        self.push_button_remove_models.setText("")
        icon1 = QtGui.QIcon()
        icon1.addPixmap(QtGui.QPixmap("../../icons/remove_circle_outline-24px.svg"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.push_button_remove_models.setIcon(icon1)
        self.push_button_remove_models.setIconSize(QtCore.QSize(18, 18))
        self.push_button_remove_models.setObjectName("push_button_remove_models")
        self.horizontalLayout_6.addWidget(self.push_button_remove_models)
        self.push_button_go = QtWidgets.QPushButton(self.tabWidget_2Page1)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.push_button_go.sizePolicy().hasHeightForWidth())
        self.push_button_go.setSizePolicy(sizePolicy)
        self.push_button_go.setText("")
        icon2 = QtGui.QIcon()
        icon2.addPixmap(QtGui.QPixmap("../../icons/play_circle_outline-24px.svg"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.push_button_go.setIcon(icon2)
        self.push_button_go.setIconSize(QtCore.QSize(18, 18))
        self.push_button_go.setObjectName("push_button_go")
        self.horizontalLayout_6.addWidget(self.push_button_go)
        self.verticalLayout_5.addLayout(self.horizontalLayout_6)
        self.list_widget_models = QtWidgets.QListWidget(self.tabWidget_2Page1)
        self.list_widget_models.setSelectionMode(QtWidgets.QAbstractItemView.ExtendedSelection)
        self.list_widget_models.setObjectName("list_widget_models")
        self.verticalLayout_5.addWidget(self.list_widget_models)
        self.verticalLayout.addLayout(self.verticalLayout_5)
        self.tabWidget_2.addTab(self.tabWidget_2Page1, "")
        self.tabWidget_2Page2 = QtWidgets.QWidget()
        self.tabWidget_2Page2.setObjectName("tabWidget_2Page2")
        self.verticalLayout_2 = QtWidgets.QVBoxLayout(self.tabWidget_2Page2)
        self.verticalLayout_2.setObjectName("verticalLayout_2")
        self.groupBox_2 = QtWidgets.QGroupBox(self.tabWidget_2Page2)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.groupBox_2.sizePolicy().hasHeightForWidth())
        self.groupBox_2.setSizePolicy(sizePolicy)
        self.groupBox_2.setObjectName("groupBox_2")
        self.verticalLayout_6 = QtWidgets.QVBoxLayout(self.groupBox_2)
        self.verticalLayout_6.setObjectName("verticalLayout_6")
        self.verticalLayout_2.addWidget(self.groupBox_2)
        self.line_edit_id = QtWidgets.QLineEdit(self.tabWidget_2Page2)
        self.line_edit_id.setText("")
        self.line_edit_id.setObjectName("line_edit_id")
        self.verticalLayout_2.addWidget(self.line_edit_id)
        self.horizontalLayout_5 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_5.setObjectName("horizontalLayout_5")
        self.push_button_add = QtWidgets.QPushButton(self.tabWidget_2Page2)
        self.push_button_add.setObjectName("push_button_add")
        self.horizontalLayout_5.addWidget(self.push_button_add)
        self.push_button_remove = QtWidgets.QPushButton(self.tabWidget_2Page2)
        self.push_button_remove.setObjectName("push_button_remove")
        self.horizontalLayout_5.addWidget(self.push_button_remove)
        self.verticalLayout_2.addLayout(self.horizontalLayout_5)
        self.tabWidget_2.addTab(self.tabWidget_2Page2, "")
        self.verticalLayout_4.addWidget(self.tabWidget_2)
        self.verticalLayout_3.addLayout(self.verticalLayout_4)
        self.horizontalLayout_4.addLayout(self.verticalLayout_3)
        self.verticalLayout_9 = QtWidgets.QVBoxLayout()
        self.verticalLayout_9.setObjectName("verticalLayout_9")
        self.graphics_view = QtWidgets.QGraphicsView(self.centralwidget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.graphics_view.sizePolicy().hasHeightForWidth())
        self.graphics_view.setSizePolicy(sizePolicy)
        self.graphics_view.setSizeAdjustPolicy(QtWidgets.QAbstractScrollArea.AdjustIgnored)
        self.graphics_view.setObjectName("graphics_view")
        self.verticalLayout_9.addWidget(self.graphics_view)
        self.horizontalLayout = QtWidgets.QHBoxLayout()
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.button_previous_page = QtWidgets.QPushButton(self.centralwidget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Minimum)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.button_previous_page.sizePolicy().hasHeightForWidth())
        self.button_previous_page.setSizePolicy(sizePolicy)
        self.button_previous_page.setObjectName("button_previous_page")
        self.horizontalLayout.addWidget(self.button_previous_page)
        self.label_page_id = QtWidgets.QLabel(self.centralwidget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.label_page_id.sizePolicy().hasHeightForWidth())
        self.label_page_id.setSizePolicy(sizePolicy)
        self.label_page_id.setAlignment(QtCore.Qt.AlignCenter)
        self.label_page_id.setObjectName("label_page_id")
        self.horizontalLayout.addWidget(self.label_page_id)
        self.button_next_page = QtWidgets.QPushButton(self.centralwidget)
        self.button_next_page.setObjectName("button_next_page")
        self.horizontalLayout.addWidget(self.button_next_page)
        self.verticalLayout_9.addLayout(self.horizontalLayout)
        self.horizontalLayout_4.addLayout(self.verticalLayout_9)
        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 1145, 22))
        self.menubar.setObjectName("menubar")
        self.menuFile = QtWidgets.QMenu(self.menubar)
        self.menuFile.setObjectName("menuFile")
        self.menuTrain = QtWidgets.QMenu(self.menubar)
        self.menuTrain.setObjectName("menuTrain")
        self.menuAnalyze = QtWidgets.QMenu(self.menubar)
        self.menuAnalyze.setObjectName("menuAnalyze")
        self.menuFile_2 = QtWidgets.QMenu(self.menubar)
        self.menuFile_2.setObjectName("menuFile_2")
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)
        self.action_project_save = QtWidgets.QAction(MainWindow)
        icon3 = QtGui.QIcon()
        icon3.addPixmap(QtGui.QPixmap("../../icons/save-24px.svg"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.action_project_save.setIcon(icon3)
        self.action_project_save.setObjectName("action_project_save")
        self.action_project_open = QtWidgets.QAction(MainWindow)
        icon4 = QtGui.QIcon()
        icon4.addPixmap(QtGui.QPixmap("../../icons/folder_open-24px.svg"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.action_project_open.setIcon(icon4)
        self.action_project_open.setObjectName("action_project_open")
        self.action_project_add_images = QtWidgets.QAction(MainWindow)
        self.action_project_add_images.setObjectName("action_project_add_images")
        self.action_project_remove_images = QtWidgets.QAction(MainWindow)
        self.action_project_remove_images.setObjectName("action_project_remove_images")
        self.action_file_zoom_in = QtWidgets.QAction(MainWindow)
        icon5 = QtGui.QIcon()
        icon5.addPixmap(QtGui.QPixmap("../../icons/zoom_in-24px.svg"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.action_file_zoom_in.setIcon(icon5)
        self.action_file_zoom_in.setObjectName("action_file_zoom_in")
        self.action_file_zoom_out = QtWidgets.QAction(MainWindow)
        icon6 = QtGui.QIcon()
        icon6.addPixmap(QtGui.QPixmap("../../icons/zoom_out-24px.svg"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.action_file_zoom_out.setIcon(icon6)
        self.action_file_zoom_out.setObjectName("action_file_zoom_out")
        self.action_file_default_size = QtWidgets.QAction(MainWindow)
        icon7 = QtGui.QIcon()
        icon7.addPixmap(QtGui.QPixmap("../../icons/fullscreen_exit-24px.svg"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.action_file_default_size.setIcon(icon7)
        self.action_file_default_size.setObjectName("action_file_default_size")
        self.action_file_delete_polygon = QtWidgets.QAction(MainWindow)
        icon8 = QtGui.QIcon()
        icon8.addPixmap(QtGui.QPixmap("../../icons/delete-24px.svg"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.action_file_delete_polygon.setIcon(icon8)
        self.action_file_delete_polygon.setObjectName("action_file_delete_polygon")
        self.action_train_train = QtWidgets.QAction(MainWindow)
        icon9 = QtGui.QIcon()
        icon9.addPixmap(QtGui.QPixmap("../../icons/play_arrow-24px.svg"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.action_train_train.setIcon(icon9)
        self.action_train_train.setObjectName("action_train_train")
        self.action_train_edit_configurations = QtWidgets.QAction(MainWindow)
        icon10 = QtGui.QIcon()
        icon10.addPixmap(QtGui.QPixmap("../../icons/build-24px.svg"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.action_train_edit_configurations.setIcon(icon10)
        self.action_train_edit_configurations.setObjectName("action_train_edit_configurations")
        self.action_analyze_tensorboard = QtWidgets.QAction(MainWindow)
        icon11 = QtGui.QIcon()
        icon11.addPixmap(QtGui.QPixmap("../../icons/show_chart-24px.svg"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.action_analyze_tensorboard.setIcon(icon11)
        self.action_analyze_tensorboard.setObjectName("action_analyze_tensorboard")
        self.action_project_new = QtWidgets.QAction(MainWindow)
        icon12 = QtGui.QIcon()
        icon12.addPixmap(QtGui.QPixmap("../../icons/add-24px.svg"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.action_project_new.setIcon(icon12)
        self.action_project_new.setObjectName("action_project_new")
        self.menuFile.addAction(self.action_project_new)
        self.menuFile.addAction(self.action_project_open)
        self.menuFile.addAction(self.action_project_save)
        self.menuFile.addSeparator()
        self.menuFile.addAction(self.action_project_add_images)
        self.menuFile.addAction(self.action_project_remove_images)
        self.menuTrain.addAction(self.action_train_train)
        self.menuTrain.addAction(self.action_train_edit_configurations)
        self.menuAnalyze.addAction(self.action_analyze_tensorboard)
        self.menuFile_2.addSeparator()
        self.menuFile_2.addAction(self.action_file_zoom_in)
        self.menuFile_2.addAction(self.action_file_zoom_out)
        self.menuFile_2.addSeparator()
        self.menuFile_2.addAction(self.action_file_default_size)
        self.menuFile_2.addSeparator()
        self.menuFile_2.addAction(self.action_file_delete_polygon)
        self.menubar.addAction(self.menuFile.menuAction())
        self.menubar.addAction(self.menuFile_2.menuAction())
        self.menubar.addAction(self.menuTrain.menuAction())
        self.menubar.addAction(self.menuAnalyze.menuAction())

        self.retranslateUi(MainWindow)
        self.tabWidget_2.setCurrentIndex(1)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "MainWindow"))
        self.sdfLabel.setText(_translate("MainWindow", "Name: "))
        self.project_name.setText(_translate("MainWindow", "TextLabel"))
        self.push_button_add_images.setText(_translate("MainWindow", "Add Images"))
        self.push_button_add_images.setShortcut(_translate("MainWindow", "Ctrl+A"))
        self.push_button_remove_images.setText(_translate("MainWindow", "Remove Images"))
        self.push_button_remove_images.setShortcut(_translate("MainWindow", "Ctrl+R"))
        self.label.setText(_translate("MainWindow", "Existed Model: "))
        self.push_button_add_models.setShortcut(_translate("MainWindow", "Shift+A"))
        self.push_button_remove_models.setShortcut(_translate("MainWindow", "Shift+R"))
        self.push_button_go.setShortcut(_translate("MainWindow", "Shift+R"))
        self.tabWidget_2.setTabText(self.tabWidget_2.indexOf(self.tabWidget_2Page1), _translate("MainWindow", "Automatically"))
        self.groupBox_2.setTitle(_translate("MainWindow", "Attributes"))
        self.push_button_add.setText(_translate("MainWindow", "Add"))
        self.push_button_remove.setText(_translate("MainWindow", "Remove"))
        self.tabWidget_2.setTabText(self.tabWidget_2.indexOf(self.tabWidget_2Page2), _translate("MainWindow", "Maually"))
        self.button_previous_page.setText(_translate("MainWindow", "Previous"))
        self.button_previous_page.setShortcut(_translate("MainWindow", "Left"))
        self.label_page_id.setText(_translate("MainWindow", "-- / --"))
        self.button_next_page.setText(_translate("MainWindow", "Next"))
        self.button_next_page.setShortcut(_translate("MainWindow", "Right"))
        self.menuFile.setTitle(_translate("MainWindow", "Project"))
        self.menuTrain.setTitle(_translate("MainWindow", "Train"))
        self.menuAnalyze.setTitle(_translate("MainWindow", "Analyze"))
        self.menuFile_2.setTitle(_translate("MainWindow", "File"))
        self.action_project_save.setText(_translate("MainWindow", "Save"))
        self.action_project_save.setStatusTip(_translate("MainWindow", "Save the project."))
        self.action_project_save.setShortcut(_translate("MainWindow", "Ctrl+S"))
        self.action_project_open.setText(_translate("MainWindow", "Open"))
        self.action_project_open.setStatusTip(_translate("MainWindow", "Open an existed project."))
        self.action_project_open.setShortcut(_translate("MainWindow", "Ctrl+L"))
        self.action_project_add_images.setText(_translate("MainWindow", "Add Images"))
        self.action_project_add_images.setStatusTip(_translate("MainWindow", "Add images."))
        self.action_project_remove_images.setText(_translate("MainWindow", "Remove Image"))
        self.action_project_remove_images.setStatusTip(_translate("MainWindow", "Remove image."))
        self.action_file_zoom_in.setText(_translate("MainWindow", "Zoom In"))
        self.action_file_zoom_out.setText(_translate("MainWindow", "Zoom Out"))
        self.action_file_default_size.setText(_translate("MainWindow", "Default Size"))
        self.action_file_delete_polygon.setText(_translate("MainWindow", "Delete Polygon"))
        self.action_train_train.setText(_translate("MainWindow", "Train"))
        self.action_train_train.setShortcut(_translate("MainWindow", "Ctrl+T"))
        self.action_train_edit_configurations.setText(_translate("MainWindow", "Edit Configurations"))
        self.action_train_edit_configurations.setShortcut(_translate("MainWindow", "Ctrl+E"))
        self.action_analyze_tensorboard.setText(_translate("MainWindow", "Tensorboard"))
        self.action_analyze_tensorboard.setShortcut(_translate("MainWindow", "Ctrl+T"))
        self.action_project_new.setText(_translate("MainWindow", "New"))
        self.action_project_new.setStatusTip(_translate("MainWindow", "Create a new project."))
        self.action_project_new.setShortcut(_translate("MainWindow", "Ctrl+N"))

