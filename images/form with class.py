import sys
from PyQt5.QtWidgets import QApplication,QMainWindow,QAction
from PyQt5.QtGui import QIcon
class GUI(QMainWindow):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        self.setWindowTitle("PyQt GUI")
        self.resize(400,300)
        self.statusBar().showMessage('Text in statubar')
        
        menubar = self.menuBar()
        new_icon1=QIcon("c.png")
        tools_icon1=QIcon("set.png")
        exit_icon1=QIcon("exit.png")
        help_icon1=QIcon("sun.png")
        file_menu = menubar.addMenu('File')
        new1_action = QAction(new_icon1,'New',self)
        new2_action = QAction('Save',self)
        Exit_action = QAction( exit_icon1,'Exit',self)
        file_menu.addAction(new1_action)
        file_menu.addSeparator()
        file_menu.addAction(new2_action)
        #**************************************************
        file_menu.addSeparator()
        Exit_action.triggered.connect(self.close)
        Exit_action.setShortcut('Ctrl+Q')
        file_menu.addAction(Exit_action)
        file_menu.addSeparator()
        #***************************************************
        tools_menu = menubar.addMenu('Tools')
        tools1_action = QAction(tools_icon1,'Option',self)
        tools_menu.addAction(tools1_action)
        
        help_menu = menubar.addMenu('Help')
        help1_action = QAction(help_icon1,'About',self)
        help_menu.addAction(help1_action)
        #new_action.setStatusTip('New')
        #new_action.setStatusTip('Save')
'------------------- Main Block ------------------------------------'
if __name__ == '__main__':
    app = QApplication(sys.argv)
    gui = GUI()
    gui.show()
    sys.exit(app.exec_())
