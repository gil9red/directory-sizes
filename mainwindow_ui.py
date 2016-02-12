# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'mainwindow.ui'
#
# Created: Fri Feb 12 16:21:13 2016
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
        self.treeView = QtGui.QTreeView(self.centralwidget)
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
        self.dockWidget = QtGui.QDockWidget(MainWindow)
        self.dockWidget.setObjectName("dockWidget")
        self.dockWidgetContents = QtGui.QWidget()
        self.dockWidgetContents.setObjectName("dockWidgetContents")
        self.verticalLayout_2 = QtGui.QVBoxLayout(self.dockWidgetContents)
        self.verticalLayout_2.setObjectName("verticalLayout_2")
        self.textEdit = QtGui.QTextEdit(self.dockWidgetContents)
        self.textEdit.setObjectName("textEdit")
        self.verticalLayout_2.addWidget(self.textEdit)
        self.dockWidget.setWidget(self.dockWidgetContents)
        MainWindow.addDockWidget(QtCore.Qt.DockWidgetArea(2), self.dockWidget)
        self.menubar.addAction(self.menuDockWindow.menuAction())
        self.menubar.addAction(self.menuTools.menuAction())

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        MainWindow.setWindowTitle(QtGui.QApplication.translate("MainWindow", "directory-sizes", None, QtGui.QApplication.UnicodeUTF8))
        self.menuDockWindow.setTitle(QtGui.QApplication.translate("MainWindow", "Окна", None, QtGui.QApplication.UnicodeUTF8))
        self.menuTools.setTitle(QtGui.QApplication.translate("MainWindow", "Tools", None, QtGui.QApplication.UnicodeUTF8))
        self.toolBarGeneral.setWindowTitle(QtGui.QApplication.translate("MainWindow", "General", None, QtGui.QApplication.UnicodeUTF8))

