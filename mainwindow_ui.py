# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'mainwindow.ui'
#
# Created: Fri Feb 19 11:43:10 2016
#      by: pyside-uic 0.2.15 running on PySide 1.2.4
#
# WARNING! All changes made in this file will be lost!

from PySide import QtCore, QtGui

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(847, 573)
        self.centralwidget = QtGui.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.verticalLayout = QtGui.QVBoxLayout(self.centralwidget)
        self.verticalLayout.setObjectName("verticalLayout")
        self.label_root_dir = QtGui.QLabel(self.centralwidget)
        self.label_root_dir.setText("")
        self.label_root_dir.setObjectName("label_root_dir")
        self.verticalLayout.addWidget(self.label_root_dir)
        self.treeView = QtGui.QTreeView(self.centralwidget)
        self.treeView.setExpandsOnDoubleClick(False)
        self.treeView.setObjectName("treeView")
        self.verticalLayout.addWidget(self.treeView)
        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtGui.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 847, 21))
        self.menubar.setObjectName("menubar")
        self.menuDockWindow = QtGui.QMenu(self.menubar)
        self.menuDockWindow.setObjectName("menuDockWindow")
        self.menuTools = QtGui.QMenu(self.menubar)
        self.menuTools.setObjectName("menuTools")
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QtGui.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)
        self.toolBarGeneral = QtGui.QToolBar(MainWindow)
        self.toolBarGeneral.setObjectName("toolBarGeneral")
        MainWindow.addToolBar(QtCore.Qt.TopToolBarArea, self.toolBarGeneral)
        self.dockWidgetSettings = QtGui.QDockWidget(MainWindow)
        self.dockWidgetSettings.setObjectName("dockWidgetSettings")
        self.dockWidgetContents_3 = QtGui.QWidget()
        self.dockWidgetContents_3.setObjectName("dockWidgetContents_3")
        self.verticalLayout_3 = QtGui.QVBoxLayout(self.dockWidgetContents_3)
        self.verticalLayout_3.setObjectName("verticalLayout_3")
        self.formLayout = QtGui.QFormLayout()
        self.formLayout.setFieldGrowthPolicy(QtGui.QFormLayout.AllNonFixedFieldsGrow)
        self.formLayout.setObjectName("formLayout")
        self.label = QtGui.QLabel(self.dockWidgetContents_3)
        self.label.setObjectName("label")
        self.formLayout.setWidget(0, QtGui.QFormLayout.LabelRole, self.label)
        self.horizontalLayout = QtGui.QHBoxLayout()
        self.horizontalLayout.setSpacing(0)
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.line_edit_dir_path = QtGui.QLineEdit(self.dockWidgetContents_3)
        self.line_edit_dir_path.setObjectName("line_edit_dir_path")
        self.horizontalLayout.addWidget(self.line_edit_dir_path)
        self.button_select_dir = QtGui.QToolButton(self.dockWidgetContents_3)
        self.button_select_dir.setObjectName("button_select_dir")
        self.horizontalLayout.addWidget(self.button_select_dir)
        self.formLayout.setLayout(0, QtGui.QFormLayout.FieldRole, self.horizontalLayout)
        self.label_min_size = QtGui.QLabel(self.dockWidgetContents_3)
        self.label_min_size.setObjectName("label_min_size")
        self.formLayout.setWidget(1, QtGui.QFormLayout.LabelRole, self.label_min_size)
        self.line_edit_filter_size = QtGui.QLineEdit(self.dockWidgetContents_3)
        self.line_edit_filter_size.setObjectName("line_edit_filter_size")
        self.formLayout.setWidget(1, QtGui.QFormLayout.FieldRole, self.line_edit_filter_size)
        self.verticalLayout_3.addLayout(self.formLayout)
        self.dockWidgetSettings.setWidget(self.dockWidgetContents_3)
        MainWindow.addDockWidget(QtCore.Qt.DockWidgetArea(2), self.dockWidgetSettings)
        self.dockWidgetLog = QtGui.QDockWidget(MainWindow)
        self.dockWidgetLog.setObjectName("dockWidgetLog")
        self.dockWidgetContents = QtGui.QWidget()
        self.dockWidgetContents.setObjectName("dockWidgetContents")
        self.verticalLayout_2 = QtGui.QVBoxLayout(self.dockWidgetContents)
        self.verticalLayout_2.setObjectName("verticalLayout_2")
        self.textEdit = QtGui.QTextEdit(self.dockWidgetContents)
        self.textEdit.setObjectName("textEdit")
        self.verticalLayout_2.addWidget(self.textEdit)
        self.dockWidgetLog.setWidget(self.dockWidgetContents)
        MainWindow.addDockWidget(QtCore.Qt.DockWidgetArea(2), self.dockWidgetLog)
        self.action_go = QtGui.QAction(MainWindow)
        self.action_go.setObjectName("action_go")
        self.action_show_in_explorer = QtGui.QAction(MainWindow)
        self.action_show_in_explorer.setObjectName("action_show_in_explorer")
        self.menubar.addAction(self.menuDockWindow.menuAction())
        self.menubar.addAction(self.menuTools.menuAction())
        self.toolBarGeneral.addAction(self.action_go)
        self.toolBarGeneral.addAction(self.action_show_in_explorer)

        self.retranslateUi(MainWindow)
        QtCore.QObject.connect(self.line_edit_dir_path, QtCore.SIGNAL("textChanged(QString)"), self.label_root_dir.setText)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        MainWindow.setWindowTitle(QtGui.QApplication.translate("MainWindow", "directory-sizes", None, QtGui.QApplication.UnicodeUTF8))
        self.menuDockWindow.setTitle(QtGui.QApplication.translate("MainWindow", "Окна", None, QtGui.QApplication.UnicodeUTF8))
        self.menuTools.setTitle(QtGui.QApplication.translate("MainWindow", "Tools", None, QtGui.QApplication.UnicodeUTF8))
        self.toolBarGeneral.setWindowTitle(QtGui.QApplication.translate("MainWindow", "General", None, QtGui.QApplication.UnicodeUTF8))
        self.dockWidgetSettings.setWindowTitle(QtGui.QApplication.translate("MainWindow", "Settings", None, QtGui.QApplication.UnicodeUTF8))
        self.label.setText(QtGui.QApplication.translate("MainWindow", "Dir:", None, QtGui.QApplication.UnicodeUTF8))
        self.line_edit_dir_path.setText(QtGui.QApplication.translate("MainWindow", "C:\\", None, QtGui.QApplication.UnicodeUTF8))
        self.button_select_dir.setToolTip(QtGui.QApplication.translate("MainWindow", "Select dir", None, QtGui.QApplication.UnicodeUTF8))
        self.button_select_dir.setText(QtGui.QApplication.translate("MainWindow", "...", None, QtGui.QApplication.UnicodeUTF8))
        self.label_min_size.setText(QtGui.QApplication.translate("MainWindow", "Filter size:", None, QtGui.QApplication.UnicodeUTF8))
        self.line_edit_filter_size.setToolTip(QtGui.QApplication.translate("MainWindow", "<html><head/><body><p>Пример: {size} &gt;= %1GB% and {size} &lt;= %3GB%</p><p>size: размер папок в байтах, который будет подставляться в {size}</p></body></html>", None, QtGui.QApplication.UnicodeUTF8))
        self.line_edit_filter_size.setText(QtGui.QApplication.translate("MainWindow", "{size} >= %1GB%", None, QtGui.QApplication.UnicodeUTF8))
        self.dockWidgetLog.setWindowTitle(QtGui.QApplication.translate("MainWindow", "Log", None, QtGui.QApplication.UnicodeUTF8))
        self.action_go.setText(QtGui.QApplication.translate("MainWindow", "Go", None, QtGui.QApplication.UnicodeUTF8))
        self.action_go.setToolTip(QtGui.QApplication.translate("MainWindow", "Go", None, QtGui.QApplication.UnicodeUTF8))
        self.action_show_in_explorer.setText(QtGui.QApplication.translate("MainWindow", "Show in Explorer", None, QtGui.QApplication.UnicodeUTF8))
        self.action_show_in_explorer.setToolTip(QtGui.QApplication.translate("MainWindow", "Show in Explorer", None, QtGui.QApplication.UnicodeUTF8))

