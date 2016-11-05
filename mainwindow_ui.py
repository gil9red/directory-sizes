# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'mainwindow.ui'
#
# Created by: PyQt4 UI code generator 4.11.4
#
# WARNING! All changes made in this file will be lost!

from PyQt4 import QtCore, QtGui

try:
    _fromUtf8 = QtCore.QString.fromUtf8
except AttributeError:
    def _fromUtf8(s):
        return s

try:
    _encoding = QtGui.QApplication.UnicodeUTF8
    def _translate(context, text, disambig):
        return QtGui.QApplication.translate(context, text, disambig, _encoding)
except AttributeError:
    def _translate(context, text, disambig):
        return QtGui.QApplication.translate(context, text, disambig)

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName(_fromUtf8("MainWindow"))
        MainWindow.resize(847, 573)
        self.centralwidget = QtGui.QWidget(MainWindow)
        self.centralwidget.setObjectName(_fromUtf8("centralwidget"))
        self.verticalLayout = QtGui.QVBoxLayout(self.centralwidget)
        self.verticalLayout.setObjectName(_fromUtf8("verticalLayout"))
        self.label_root_dir = QtGui.QLabel(self.centralwidget)
        self.label_root_dir.setText(_fromUtf8(""))
        self.label_root_dir.setObjectName(_fromUtf8("label_root_dir"))
        self.verticalLayout.addWidget(self.label_root_dir)
        self.treeView = QtGui.QTreeView(self.centralwidget)
        self.treeView.setExpandsOnDoubleClick(False)
        self.treeView.setObjectName(_fromUtf8("treeView"))
        self.verticalLayout.addWidget(self.treeView)
        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtGui.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 847, 21))
        self.menubar.setObjectName(_fromUtf8("menubar"))
        self.menuDockWindow = QtGui.QMenu(self.menubar)
        self.menuDockWindow.setObjectName(_fromUtf8("menuDockWindow"))
        self.menuTools = QtGui.QMenu(self.menubar)
        self.menuTools.setObjectName(_fromUtf8("menuTools"))
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QtGui.QStatusBar(MainWindow)
        self.statusbar.setObjectName(_fromUtf8("statusbar"))
        MainWindow.setStatusBar(self.statusbar)
        self.toolBarGeneral = QtGui.QToolBar(MainWindow)
        self.toolBarGeneral.setObjectName(_fromUtf8("toolBarGeneral"))
        MainWindow.addToolBar(QtCore.Qt.TopToolBarArea, self.toolBarGeneral)
        self.dockWidgetSettings = QtGui.QDockWidget(MainWindow)
        self.dockWidgetSettings.setObjectName(_fromUtf8("dockWidgetSettings"))
        self.dockWidgetContents_3 = QtGui.QWidget()
        self.dockWidgetContents_3.setObjectName(_fromUtf8("dockWidgetContents_3"))
        self.verticalLayout_3 = QtGui.QVBoxLayout(self.dockWidgetContents_3)
        self.verticalLayout_3.setObjectName(_fromUtf8("verticalLayout_3"))
        self.formLayout = QtGui.QFormLayout()
        self.formLayout.setFieldGrowthPolicy(QtGui.QFormLayout.AllNonFixedFieldsGrow)
        self.formLayout.setObjectName(_fromUtf8("formLayout"))
        self.label = QtGui.QLabel(self.dockWidgetContents_3)
        self.label.setObjectName(_fromUtf8("label"))
        self.formLayout.setWidget(0, QtGui.QFormLayout.LabelRole, self.label)
        self.horizontalLayout = QtGui.QHBoxLayout()
        self.horizontalLayout.setSpacing(0)
        self.horizontalLayout.setObjectName(_fromUtf8("horizontalLayout"))
        self.line_edit_dir_path = QtGui.QLineEdit(self.dockWidgetContents_3)
        self.line_edit_dir_path.setObjectName(_fromUtf8("line_edit_dir_path"))
        self.horizontalLayout.addWidget(self.line_edit_dir_path)
        self.button_select_dir = QtGui.QToolButton(self.dockWidgetContents_3)
        self.button_select_dir.setObjectName(_fromUtf8("button_select_dir"))
        self.horizontalLayout.addWidget(self.button_select_dir)
        self.formLayout.setLayout(0, QtGui.QFormLayout.FieldRole, self.horizontalLayout)
        self.label_min_size = QtGui.QLabel(self.dockWidgetContents_3)
        self.label_min_size.setObjectName(_fromUtf8("label_min_size"))
        self.formLayout.setWidget(1, QtGui.QFormLayout.LabelRole, self.label_min_size)
        self.line_edit_filter = QtGui.QLineEdit(self.dockWidgetContents_3)
        self.line_edit_filter.setObjectName(_fromUtf8("line_edit_filter"))
        self.formLayout.setWidget(1, QtGui.QFormLayout.FieldRole, self.line_edit_filter)
        self.label_2 = QtGui.QLabel(self.dockWidgetContents_3)
        self.label_2.setObjectName(_fromUtf8("label_2"))
        self.formLayout.setWidget(2, QtGui.QFormLayout.LabelRole, self.label_2)
        self.check_box_auto_apply_filter = QtGui.QCheckBox(self.dockWidgetContents_3)
        self.check_box_auto_apply_filter.setText(_fromUtf8(""))
        self.check_box_auto_apply_filter.setChecked(True)
        self.check_box_auto_apply_filter.setObjectName(_fromUtf8("check_box_auto_apply_filter"))
        self.formLayout.setWidget(2, QtGui.QFormLayout.FieldRole, self.check_box_auto_apply_filter)
        self.verticalLayout_3.addLayout(self.formLayout)
        self.dockWidgetSettings.setWidget(self.dockWidgetContents_3)
        MainWindow.addDockWidget(QtCore.Qt.DockWidgetArea(2), self.dockWidgetSettings)
        self.action_go = QtGui.QAction(MainWindow)
        self.action_go.setObjectName(_fromUtf8("action_go"))
        self.action_show_in_explorer = QtGui.QAction(MainWindow)
        self.action_show_in_explorer.setObjectName(_fromUtf8("action_show_in_explorer"))
        self.action_apply_filter = QtGui.QAction(MainWindow)
        self.action_apply_filter.setObjectName(_fromUtf8("action_apply_filter"))
        self.menubar.addAction(self.menuDockWindow.menuAction())
        self.menubar.addAction(self.menuTools.menuAction())
        self.toolBarGeneral.addAction(self.action_go)
        self.toolBarGeneral.addAction(self.action_apply_filter)
        self.toolBarGeneral.addAction(self.action_show_in_explorer)

        self.retranslateUi(MainWindow)
        QtCore.QObject.connect(self.line_edit_dir_path, QtCore.SIGNAL(_fromUtf8("textChanged(QString)")), self.label_root_dir.setText)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        MainWindow.setWindowTitle(_translate("MainWindow", "directory-sizes", None))
        self.menuDockWindow.setTitle(_translate("MainWindow", "Окна", None))
        self.menuTools.setTitle(_translate("MainWindow", "Tools", None))
        self.toolBarGeneral.setWindowTitle(_translate("MainWindow", "General", None))
        self.dockWidgetSettings.setWindowTitle(_translate("MainWindow", "Settings", None))
        self.label.setText(_translate("MainWindow", "Dir:", None))
        self.line_edit_dir_path.setText(_translate("MainWindow", "C:\\", None))
        self.button_select_dir.setToolTip(_translate("MainWindow", "Select dir", None))
        self.button_select_dir.setText(_translate("MainWindow", "...", None))
        self.label_min_size.setText(_translate("MainWindow", "Filter:", None))
        self.line_edit_filter.setToolTip(_translate("MainWindow", "<html><head/><body><p>Пример: {size} &gt;= %1GB% and {size} &lt;= %3GB%</p><p>size: размер папок в байтах, который будет подставляться в {size}</p></body></html>", None))
        self.line_edit_filter.setText(_translate("MainWindow", "{size} >= %1GB%", None))
        self.label_2.setText(_translate("MainWindow", "Auto apply filter", None))
        self.action_go.setText(_translate("MainWindow", "Go", None))
        self.action_go.setToolTip(_translate("MainWindow", "Go", None))
        self.action_show_in_explorer.setText(_translate("MainWindow", "Show in Explorer", None))
        self.action_show_in_explorer.setToolTip(_translate("MainWindow", "Show in Explorer", None))
        self.action_apply_filter.setText(_translate("MainWindow", "Apply Filter", None))

