import sys
from PyQt5.QtWidgets import *
app = QApplication (sys.argv)
win = QWidget()
win.resize(500,300)
win.setWindowTitle('This is a programming')
win.show()
app.exec_()

