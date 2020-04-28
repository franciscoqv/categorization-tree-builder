# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'uiscroll.ui'
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
        MainWindow.setEnabled(True)
        MainWindow.resize(1000, 700)
        MainWindow.setMinimumSize(QtCore.QSize(1000, 700))
        self.centralwidget = QtGui.QWidget(MainWindow)
        self.centralwidget.setObjectName(_fromUtf8("centralwidget"))
        self.horizontalLayout = QtGui.QHBoxLayout(self.centralwidget)
        self.horizontalLayout.setObjectName(_fromUtf8("horizontalLayout"))
        self.optionsWidget = QtGui.QWidget(self.centralwidget)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Fixed, QtGui.QSizePolicy.Minimum)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.optionsWidget.sizePolicy().hasHeightForWidth())
        self.optionsWidget.setSizePolicy(sizePolicy)
        self.optionsWidget.setMinimumSize(QtCore.QSize(230, 500))
        self.optionsWidget.setObjectName(_fromUtf8("optionsWidget"))
        self.datasetBox = QtGui.QGroupBox(self.optionsWidget)
        self.datasetBox.setGeometry(QtCore.QRect(10, 10, 211, 91))
        self.datasetBox.setObjectName(_fromUtf8("datasetBox"))
        self.datasetText = QtGui.QLineEdit(self.datasetBox)
        self.datasetText.setGeometry(QtCore.QRect(10, 20, 191, 20))
        self.datasetText.setReadOnly(True)
        self.datasetText.setObjectName(_fromUtf8("datasetText"))
        self.loadDatasetButton = QtGui.QPushButton(self.datasetBox)
        self.loadDatasetButton.setGeometry(QtCore.QRect(10, 50, 191, 23))
        self.loadDatasetButton.setObjectName(_fromUtf8("loadDatasetButton"))
        self.treeBox = QtGui.QGroupBox(self.optionsWidget)
        self.treeBox.setGeometry(QtCore.QRect(10, 270, 211, 91))
        self.treeBox.setObjectName(_fromUtf8("treeBox"))
        self.saveTreeButton = QtGui.QPushButton(self.treeBox)
        self.saveTreeButton.setEnabled(False)
        self.saveTreeButton.setGeometry(QtCore.QRect(10, 20, 191, 23))
        self.saveTreeButton.setObjectName(_fromUtf8("saveTreeButton"))
        self.loadTreeButton = QtGui.QPushButton(self.treeBox)
        self.loadTreeButton.setEnabled(False)
        self.loadTreeButton.setGeometry(QtCore.QRect(10, 50, 191, 23))
        self.loadTreeButton.setObjectName(_fromUtf8("loadTreeButton"))
        self.categoryBox = QtGui.QGroupBox(self.optionsWidget)
        self.categoryBox.setGeometry(QtCore.QRect(10, 110, 211, 151))
        self.categoryBox.setObjectName(_fromUtf8("categoryBox"))
        self.categoryCombo = QtGui.QComboBox(self.categoryBox)
        self.categoryCombo.setEnabled(False)
        self.categoryCombo.setGeometry(QtCore.QRect(10, 40, 191, 22))
        self.categoryCombo.setObjectName(_fromUtf8("categoryCombo"))
        self.categoryLabel = QtGui.QLabel(self.categoryBox)
        self.categoryLabel.setGeometry(QtCore.QRect(10, 20, 191, 16))
        self.categoryLabel.setObjectName(_fromUtf8("categoryLabel"))
        self.trueValueLabel = QtGui.QLabel(self.categoryBox)
        self.trueValueLabel.setGeometry(QtCore.QRect(10, 80, 191, 16))
        self.trueValueLabel.setObjectName(_fromUtf8("trueValueLabel"))
        self.trueValueCombo = QtGui.QComboBox(self.categoryBox)
        self.trueValueCombo.setEnabled(False)
        self.trueValueCombo.setGeometry(QtCore.QRect(10, 100, 191, 22))
        self.trueValueCombo.setObjectName(_fromUtf8("trueValueCombo"))
        self.statisticsLabel = QtGui.QLabel(self.optionsWidget)
        self.statisticsLabel.setGeometry(QtCore.QRect(20, 380, 191, 201))
        self.statisticsLabel.setText(_fromUtf8(""))
        self.statisticsLabel.setAlignment(QtCore.Qt.AlignLeading|QtCore.Qt.AlignLeft|QtCore.Qt.AlignTop)
        self.statisticsLabel.setObjectName(_fromUtf8("statisticsLabel"))
        self.horizontalLayout.addWidget(self.optionsWidget)
        self.scrollArea = QtGui.QScrollArea(self.centralwidget)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Minimum, QtGui.QSizePolicy.Minimum)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.scrollArea.sizePolicy().hasHeightForWidth())
        self.scrollArea.setSizePolicy(sizePolicy)
        self.scrollArea.setMinimumSize(QtCore.QSize(500, 500))
        self.scrollArea.setVerticalScrollBarPolicy(QtCore.Qt.ScrollBarAsNeeded)
        self.scrollArea.setHorizontalScrollBarPolicy(QtCore.Qt.ScrollBarAsNeeded)
        self.scrollArea.setWidgetResizable(True)
        self.scrollArea.setObjectName(_fromUtf8("scrollArea"))
        self.scrollAreaWidgetContents_2 = QtGui.QWidget()
        self.scrollAreaWidgetContents_2.setGeometry(QtCore.QRect(0, 0, 744, 639))
        self.scrollAreaWidgetContents_2.setObjectName(_fromUtf8("scrollAreaWidgetContents_2"))
        self.scrollArea.setWidget(self.scrollAreaWidgetContents_2)
        self.horizontalLayout.addWidget(self.scrollArea)
        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtGui.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 1000, 21))
        self.menubar.setObjectName(_fromUtf8("menubar"))
        self.menuFast_and_frugal_tree_creator = QtGui.QMenu(self.menubar)
        self.menuFast_and_frugal_tree_creator.setObjectName(_fromUtf8("menuFast_and_frugal_tree_creator"))
        self.menuOptimize = QtGui.QMenu(self.menubar)
        self.menuOptimize.setObjectName(_fromUtf8("menuOptimize"))
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QtGui.QStatusBar(MainWindow)
        self.statusbar.setObjectName(_fromUtf8("statusbar"))
        MainWindow.setStatusBar(self.statusbar)
        self.actionLoad_new_dataset = QtGui.QAction(MainWindow)
        self.actionLoad_new_dataset.setObjectName(_fromUtf8("actionLoad_new_dataset"))
        self.actionSave_current_tree = QtGui.QAction(MainWindow)
        self.actionSave_current_tree.setEnabled(False)
        self.actionSave_current_tree.setObjectName(_fromUtf8("actionSave_current_tree"))
        self.actionLoad_tree = QtGui.QAction(MainWindow)
        self.actionLoad_tree.setEnabled(False)
        self.actionLoad_tree.setObjectName(_fromUtf8("actionLoad_tree"))
        self.actionNew_tree = QtGui.QAction(MainWindow)
        self.actionNew_tree.setEnabled(False)
        self.actionNew_tree.setObjectName(_fromUtf8("actionNew_tree"))
        self.actionGreedy_tree_optimization = QtGui.QAction(MainWindow)
        self.actionGreedy_tree_optimization.setObjectName(_fromUtf8("actionGreedy_tree_optimization"))
        self.menuFast_and_frugal_tree_creator.addAction(self.actionLoad_new_dataset)
        self.menuFast_and_frugal_tree_creator.addSeparator()
        self.menuFast_and_frugal_tree_creator.addAction(self.actionSave_current_tree)
        self.menuFast_and_frugal_tree_creator.addAction(self.actionLoad_tree)
        self.menuFast_and_frugal_tree_creator.addAction(self.actionNew_tree)
        self.menuOptimize.addAction(self.actionGreedy_tree_optimization)
        self.menubar.addAction(self.menuFast_and_frugal_tree_creator.menuAction())
        self.menubar.addAction(self.menuOptimize.menuAction())

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        MainWindow.setWindowTitle(_translate("MainWindow", "Fast-and-frugal Tree Builder", None))
        self.datasetBox.setTitle(_translate("MainWindow", "Dataset file", None))
        self.loadDatasetButton.setText(_translate("MainWindow", "Load dataset", None))
        self.treeBox.setTitle(_translate("MainWindow", "Tree", None))
        self.saveTreeButton.setText(_translate("MainWindow", "Save current tree", None))
        self.loadTreeButton.setText(_translate("MainWindow", "Load tree", None))
        self.categoryBox.setTitle(_translate("MainWindow", "Category settings", None))
        self.categoryLabel.setText(_translate("MainWindow", "Category", None))
        self.trueValueLabel.setText(_translate("MainWindow", "Correct category value for left nodes", None))
        self.menuFast_and_frugal_tree_creator.setTitle(_translate("MainWindow", "File", None))
        self.menuOptimize.setTitle(_translate("MainWindow", "Optimize", None))
        self.actionLoad_new_dataset.setText(_translate("MainWindow", "Load dataset...", None))
        self.actionSave_current_tree.setText(_translate("MainWindow", "Save current tree...", None))
        self.actionLoad_tree.setText(_translate("MainWindow", "Load tree...", None))
        self.actionNew_tree.setText(_translate("MainWindow", "New tree", None))
        self.actionGreedy_tree_optimization.setText(_translate("MainWindow", "Greedy tree optimization", None))


class MainWindow(QtGui.QMainWindow, Ui_MainWindow):
    def __init__(self, parent=None, f=QtCore.Qt.WindowFlags()):
        QtGui.QMainWindow.__init__(self, parent, f)

        self.setupUi(self)

