# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'F:\PYthon\PY_PRJ\GUI_Prj\Textbox_test.ui'
#
# Created by: PyQt5 UI code generator 5.11.3
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(438, 287)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.Txt_Text = QtWidgets.QLineEdit(self.centralwidget)
        self.Txt_Text.setEnabled(True)
        self.Txt_Text.setGeometry(QtCore.QRect(120, 190, 251, 20))
        self.Txt_Text.setFocusPolicy(QtCore.Qt.StrongFocus)
        self.Txt_Text.setLayoutDirection(QtCore.Qt.RightToLeft)
        self.Txt_Text.setAutoFillBackground(False)
        self.Txt_Text.setStyleSheet("background-color: rgb(26, 255, 171);")
        self.Txt_Text.setCursorPosition(0)
        self.Txt_Text.setDragEnabled(True)
        self.Txt_Text.setClearButtonEnabled(True)
        self.Txt_Text.setObjectName("Txt_Text")


        
        self.Butt_01 = QtWidgets.QPushButton(self.centralwidget)
        self.Butt_01.setGeometry(QtCore.QRect(170, 130, 75, 23))
        self.Butt_01.setObjectName("Butt_01")
        self.Butt_01.clicked.connect(self.clickMethod)
     



        
        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 438, 21))
        self.menubar.setObjectName("menubar")
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "MainWindow"))
        self.Txt_Text.setText(_translate("MainWindow", "اطلاعات خود را اینجا وارد نمایید"))
        self.Butt_01.setText(_translate("MainWindow", "PushButton"))
    def clickMethod(self):
        print('Your name: ' + self.Txt_Text.text())

if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    MainWindow = QtWidgets.QMainWindow()
    ui = Ui_MainWindow()
    ui.setupUi(MainWindow)
    MainWindow.show()
    sys.exit(app.exec_())

