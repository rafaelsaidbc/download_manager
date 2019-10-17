# ================================== IMPORTS ==================================
import sys

from PyQt4.QtCore import *
from PyQt4.QtGui import *
from PyQt4.uic import loadUiType

from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.uic import loadUiType

import os
from os import path

import urllib.request


# ================================== IMPORT UI FILE ==================================
FROM_CLASS,_=loadUiType(path.join(path.dirname(__file__), "main.ui"))

# ================================== Initiate UI File ==================================
class MainApp(QMainWindow, FROM_CLASS):
    def __init__(self, parent=None):
        super(MainApp, self).__init__(parent)
        QMainWindow.__init__(self)
        self.setupUi(self)
        self.Handel_UI()
        self.Handel_Buttons()


    def Handel_UI(self):
        self.setWindowTitle('Rafa Downloader')


    def Handel_Buttons(self):
        self.pushButton.clicked.connect(self.Download)
        self.pushButton_2.clicked.connect(self.Handel_Browse)


    def Handel_Browse(self):
        save_place = QFileDialog.getSaveFileName(self, caption='Save AS', directory='.', filter='All files (*.*)')
        text = str(save_place)
        name = (text[2:].split(',')[0].replace("'", ''))
        self.lineEdit_2.setText(name)


    def Handel_Progress(self, blocknum, blocksize, totalsize):
        read = blocknum * blocksize
        if totalsize > 0:
            percent = read * 100 / totalsize
            self.progressBar.setValue(percent)
            QApplication.processEvents() # Not responding


    def Download(self):
        # url - save location - progress
        url = self.lineEdit.text()
        save_location = self.lineEdit_2.text()

        try:
            urllib.request.urlretrieve(url, save_location, self.Handel_Progress)
        except Exception:
            QMessageBox.warning(self, 'Erro no download!', 'O download falhou!')
            return

        QMessageBox.information(self, 'Download completo!', 'O download terminou!')
        self.progressBar.setValue(0)
        self.lineEdit.setText('')
        self.lineEdit_2.setText('')


def main():
    app = QApplication(sys.argv)
    window = MainApp()
    window.show()
    app.exec_()


if __name__ == '__main__':
    main()