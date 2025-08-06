# -*- coding: utf-8 -*-


try:
    from PyQt6.QtCore import Qt, QRect
    from PyQt6.QtGui import QAction
    from PyQt6.QtWidgets import (
        QFormLayout,
        QApplication,
        QWidget,
        QVBoxLayout,
        QHBoxLayout,
        QLabel,
        QTreeView,
        QMenuBar,
        QLineEdit,
        QMenu,
        QStatusBar,
        QToolBar,
        QDockWidget,
        QToolButton,
        QCheckBox,
    )
except ImportError:
    try:
        from PyQt5.QtCore import Qt, QRect
        from PyQt5.QtWidgets import (
            QFormLayout,
            QApplication,
            QWidget,
            QVBoxLayout,
            QHBoxLayout,
            QLabel,
            QTreeView,
            QMenuBar,
            QLineEdit,
            QMenu,
            QStatusBar,
            QToolBar,
            QDockWidget,
            QToolButton,
            QCheckBox,
            QAction,
        )
    except ImportError:
        from PyQt4.QtCore import Qt, QString, QRect
        from PyQt4.QtGui import (
            QFormLayout,
            QApplication,
            QWidget,
            QHBoxLayout,
            QLabel,
            QTreeView,
            QMenuBar,
            QLineEdit,
            QMenu,
            QStatusBar,
            QToolBar,
            QDockWidget,
            QToolButton,
            QCheckBox,
        )

try:
    Qt_TopToolBarArea = Qt.ToolBarArea.TopToolBarArea
    QFormLayout_AllNonFixedFieldsGrow = (
        QFormLayout.FieldGrowthPolicy.AllNonFixedFieldsGrow
    )
    QFormLayout_LabelRole = QFormLayout.ItemRole.LabelRole
    QFormLayout_FieldRole = QFormLayout.ItemRole.FieldRole
except AttributeError:
    Qt_TopToolBarArea = Qt.TopToolBarArea
    QFormLayout_AllNonFixedFieldsGrow = QFormLayout.AllNonFixedFieldsGrow
    QFormLayout_LabelRole = QFormLayout.LabelRole
    QFormLayout_FieldRole = QFormLayout.FieldRole

try:
    _encoding = QApplication.UnicodeUTF8

    def _translate(context, text, disambig):
        return QApplication.translate(context, text, disambig, _encoding)

except AttributeError:

    def _translate(context, text, disambig):
        return QApplication.translate(context, text, disambig)


class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(847, 573)
        self.centralwidget = QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.verticalLayout = QVBoxLayout(self.centralwidget)
        self.verticalLayout.setObjectName("verticalLayout")
        self.label_root_dir = QLabel(self.centralwidget)
        self.label_root_dir.setText("")
        self.label_root_dir.setObjectName("label_root_dir")
        self.verticalLayout.addWidget(self.label_root_dir)
        self.treeView = QTreeView(self.centralwidget)
        self.treeView.setExpandsOnDoubleClick(False)
        self.treeView.setObjectName("treeView")
        self.verticalLayout.addWidget(self.treeView)
        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QMenuBar(MainWindow)
        self.menubar.setGeometry(QRect(0, 0, 847, 21))
        self.menubar.setObjectName("menubar")
        self.menuDockWindow = QMenu(self.menubar)
        self.menuDockWindow.setObjectName("menuDockWindow")
        self.menuTools = QMenu(self.menubar)
        self.menuTools.setObjectName("menuTools")
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)
        self.toolBarGeneral = QToolBar(MainWindow)
        self.toolBarGeneral.setObjectName("toolBarGeneral")
        MainWindow.addToolBar(Qt_TopToolBarArea, self.toolBarGeneral)
        self.dockWidgetSettings = QDockWidget(MainWindow)
        self.dockWidgetSettings.setObjectName("dockWidgetSettings")
        self.dockWidgetContents_3 = QWidget()
        self.dockWidgetContents_3.setObjectName("dockWidgetContents_3")
        self.verticalLayout_3 = QVBoxLayout(self.dockWidgetContents_3)
        self.verticalLayout_3.setObjectName("verticalLayout_3")
        self.formLayout = QFormLayout()
        self.formLayout.setFieldGrowthPolicy(QFormLayout_AllNonFixedFieldsGrow)
        self.formLayout.setObjectName("formLayout")
        self.label = QLabel(self.dockWidgetContents_3)
        self.label.setObjectName("label")
        self.formLayout.setWidget(0, QFormLayout_LabelRole, self.label)
        self.horizontalLayout = QHBoxLayout()
        self.horizontalLayout.setSpacing(0)
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.line_edit_dir_path = QLineEdit(self.dockWidgetContents_3)
        self.line_edit_dir_path.setObjectName("line_edit_dir_path")
        self.horizontalLayout.addWidget(self.line_edit_dir_path)
        self.button_select_dir = QToolButton(self.dockWidgetContents_3)
        self.button_select_dir.setObjectName("button_select_dir")
        self.horizontalLayout.addWidget(self.button_select_dir)
        self.formLayout.setLayout(0, QFormLayout_FieldRole, self.horizontalLayout)
        self.label_min_size = QLabel(self.dockWidgetContents_3)
        self.label_min_size.setObjectName("label_min_size")
        self.formLayout.setWidget(1, QFormLayout_LabelRole, self.label_min_size)
        self.line_edit_filter = QLineEdit(self.dockWidgetContents_3)
        self.line_edit_filter.setObjectName("line_edit_filter")
        self.formLayout.setWidget(1, QFormLayout_FieldRole, self.line_edit_filter)
        self.label_2 = QLabel(self.dockWidgetContents_3)
        self.label_2.setObjectName("label_2")
        self.formLayout.setWidget(2, QFormLayout_LabelRole, self.label_2)
        self.check_box_auto_apply_filter = QCheckBox(self.dockWidgetContents_3)
        self.check_box_auto_apply_filter.setText("")
        self.check_box_auto_apply_filter.setChecked(True)
        self.check_box_auto_apply_filter.setObjectName("check_box_auto_apply_filter")
        self.formLayout.setWidget(
            2, QFormLayout_FieldRole, self.check_box_auto_apply_filter
        )
        self.verticalLayout_3.addLayout(self.formLayout)
        self.dockWidgetSettings.setWidget(self.dockWidgetContents_3)
        MainWindow.addDockWidget(Qt.DockWidgetArea(2), self.dockWidgetSettings)
        self.action_go = QAction(MainWindow)
        self.action_go.setObjectName("action_go")
        self.action_show_in_explorer = QAction(MainWindow)
        self.action_show_in_explorer.setObjectName("action_show_in_explorer")
        self.action_apply_filter = QAction(MainWindow)
        self.action_apply_filter.setObjectName("action_apply_filter")
        self.menubar.addAction(self.menuDockWindow.menuAction())
        self.menubar.addAction(self.menuTools.menuAction())
        self.action_about_qt = QAction(MainWindow)
        self.action_about_qt.setObjectName("action_about_qt")
        self.menubar.addAction(self.action_about_qt)
        self.toolBarGeneral.addAction(self.action_go)
        self.toolBarGeneral.addAction(self.action_apply_filter)
        self.toolBarGeneral.addAction(self.action_show_in_explorer)

        self.retranslateUi(MainWindow)
        self.line_edit_dir_path.textChanged.connect(self.label_root_dir.setText)

    def retranslateUi(self, MainWindow):
        MainWindow.setWindowTitle(_translate("MainWindow", "directory-sizes", None))
        self.menuDockWindow.setTitle(_translate("MainWindow", "Windows", None))
        self.menuTools.setTitle(_translate("MainWindow", "Tools", None))
        self.toolBarGeneral.setWindowTitle(_translate("MainWindow", "General", None))
        self.dockWidgetSettings.setWindowTitle(
            _translate("MainWindow", "Settings", None)
        )
        self.label.setText(_translate("MainWindow", "Dir:", None))
        self.line_edit_dir_path.setText(_translate("MainWindow", "C:\\", None))
        self.button_select_dir.setToolTip(_translate("MainWindow", "Select dir", None))
        self.button_select_dir.setText(_translate("MainWindow", "...", None))
        self.label_min_size.setText(_translate("MainWindow", "Filter:", None))
        self.line_edit_filter.setToolTip(
            _translate(
                "MainWindow",
                "<html><head/><body><p>Пример: {size} &gt;= %1GB% and {size} &lt;= %3GB%</p><p>size: размер папок в байтах, который будет подставляться в {size}</p></body></html>",
                None,
            )
        )
        self.line_edit_filter.setText(_translate("MainWindow", "{size} >= %1GB%", None))
        self.label_2.setText(_translate("MainWindow", "Auto apply filter", None))
        self.action_about_qt.setText(_translate("MainWindow", "About Qt", None))
        self.action_go.setText(_translate("MainWindow", "Go", None))
        self.action_go.setToolTip(_translate("MainWindow", "Go", None))
        self.action_show_in_explorer.setText(
            _translate("MainWindow", "Show in Explorer", None)
        )
        self.action_show_in_explorer.setToolTip(
            _translate("MainWindow", "Show in Explorer", None)
        )
        self.action_apply_filter.setText(_translate("MainWindow", "Apply Filter", None))
