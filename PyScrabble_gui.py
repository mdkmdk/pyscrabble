# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file '/home/mk/Workspaces/git/pyscrabble/PyScrabble.ui'
#
# Created: Wed Sep 18 06:40:59 2013
#      by: PyQt4 UI code generator 4.10.3
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

class Ui_PyScrabble(object):
    def setupUi(self, PyScrabble):
        PyScrabble.setObjectName(_fromUtf8("PyScrabble"))
        PyScrabble.resize(843, 677)
        self.centralwidget = QtGui.QWidget(PyScrabble)
        self.centralwidget.setObjectName(_fromUtf8("centralwidget"))
        self.board_frame = QtGui.QFrame(self.centralwidget)
        self.board_frame.setGeometry(QtCore.QRect(9, -1, 821, 551))
        self.board_frame.setFrameShape(QtGui.QFrame.StyledPanel)
        self.board_frame.setFrameShadow(QtGui.QFrame.Raised)
        self.board_frame.setObjectName(_fromUtf8("board_frame"))
        self.graphicsView = QtGui.QGraphicsView(self.centralwidget)
        self.graphicsView.setGeometry(QtCore.QRect(80, 580, 41, 91))
        self.graphicsView.setObjectName(_fromUtf8("graphicsView"))
        PyScrabble.setCentralWidget(self.centralwidget)
        self.menubar = QtGui.QMenuBar(PyScrabble)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 843, 27))
        self.menubar.setObjectName(_fromUtf8("menubar"))
        self.menuMenu = QtGui.QMenu(self.menubar)
        self.menuMenu.setObjectName(_fromUtf8("menuMenu"))
        PyScrabble.setMenuBar(self.menubar)
        self.statusbar = QtGui.QStatusBar(PyScrabble)
        self.statusbar.setObjectName(_fromUtf8("statusbar"))
        PyScrabble.setStatusBar(self.statusbar)
        self.toolBar = QtGui.QToolBar(PyScrabble)
        self.toolBar.setObjectName(_fromUtf8("toolBar"))
        PyScrabble.addToolBar(QtCore.Qt.TopToolBarArea, self.toolBar)
        self.actionNew_Game = QtGui.QAction(PyScrabble)
        self.actionNew_Game.setObjectName(_fromUtf8("actionNew_Game"))
        self.actionExit = QtGui.QAction(PyScrabble)
        self.actionExit.setObjectName(_fromUtf8("actionExit"))
        self.menuMenu.addSeparator()
        self.menuMenu.addAction(self.actionNew_Game)
        self.menuMenu.addAction(self.actionExit)
        self.menubar.addAction(self.menuMenu.menuAction())

        self.retranslateUi(PyScrabble)
        QtCore.QMetaObject.connectSlotsByName(PyScrabble)

    def retranslateUi(self, PyScrabble):
        PyScrabble.setWindowTitle(_translate("PyScrabble", "MainWindow", None))
        self.menuMenu.setTitle(_translate("PyScrabble", "Menu", None))
        self.toolBar.setWindowTitle(_translate("PyScrabble", "toolBar", None))
        self.actionNew_Game.setText(_translate("PyScrabble", "New Game", None))
        self.actionExit.setText(_translate("PyScrabble", "Exit", None))

