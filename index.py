# ================================== IMPORTS ==================================
import os
import sys
import urllib.request
from os import path

import humanize as humanize
import pafy
# from PyQt4.QtCore import *
# from PyQt4.QtGui import *
from PyQt5.QtWidgets import *
from PyQt5.uic import loadUiType

# ToDo: converter de vídeo pra aúdio mp3

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
        self.setWindowTitle('Rafa Said Downloader')


    def Handel_Buttons(self):
        self.pushButton.clicked.connect(self.Download)
        self.pushButton_2.clicked.connect(self.Handel_Browse)
        # botão download da aba youtube video downloader
        self.pushButton_4.clicked.connect(self.Download_Youtube_Video)
        # botão search da aba Download Youtube Video
        self.pushButton_7.clicked.connect(self.Get_Youtube_Video)
        # botão search da aba Download Youtube Playlist
        self.pushButton_8.clicked.connect(self.Get_Youtube_Video_Playlist)
        # botão browse da aba youtube video downloader
        self.pushButton_3.clicked.connect(self.Save_Browse_Video)
        # botão Start Download na aba Download Youtube Playlist
        self.pushButton_6.clicked.connect(self.Playlist_Download)
        # botão browse da aba Playlist video downloader
        self.pushButton_5.clicked.connect(self.Save_Browse_Playlist)


    def Handel_Browse(self):
        save_place = QFileDialog.getSaveFileName(self, caption='Save AS', directory='.', filter='All files (*.*)')
        text = str(save_place)
        name = (text[2:].split(',')[0].replace("'", ''))
        self.lineEdit_2.setText(name)


    def Handel_Progress(self, blocknum, blocksize, totalsize):
        read = blocknum * blocksize
        if totalsize > 0:
            percent = read * 100 / totalsize
            if self.pushButton.clicked:
                self.progressBar.setValue(percent)
                QApplication.processEvents()  # Not responding
            elif self.pushButton_4.clicked:
                self.proggressBar_2.setValu(percent)
                QApplication.processEvents()  # Not responding
            elif self.pushButton_6.clicked:
                self.progressBar_3.setValue(percent)
                QApplication.processEvents()  # Not responding


    def Download(self):
        # url - save location - progress
        url = self.lineEdit.text()
        save_location = self.lineEdit_2.text()
        try:
            urllib.request.urlretrieve(url, save_location, self.Handel_Progress)
            QApplication.processEvents()  # Not responding
        except Exception:
            QMessageBox.warning(self, 'Download Error!', 'Download Failed!')
            return
        QMessageBox.information(self, 'Download complete!', 'Download finished!')
        self.progressBar.setValue(0)
        self.lineEdit.setText('')
        self.lineEdit_2.setText('')

    def Save_Browse_Video(self):
        save = QFileDialog.getExistingDirectory(self, 'Select Download Directory')
        self.pushButton_3.clicked
        self.lineEdit_4.setText(save)
        QApplication.processEvents()  # Not responding

    def Save_Browse_Playlist(self):
        save = QFileDialog.getExistingDirectory(self, 'Select Download Directory')
        self.pushButton_5.clicked
        self.lineEdit_5.setText(save)
        QApplication.processEvents()  # Not responding

    def Get_Youtube_Video(self):
        video_link = self.lineEdit_3.text()
        v = pafy.new(video_link)
        st = v.allstreams
        for s in st:
            size = humanize.naturalsize(s.get_filesize())
            data = f'Format: {s.mediatype} - Extension: {s.extension} - Quality: {s.quality} - Size: {size}'
            self.comboBox.addItem(data)

    def Get_Youtube_Video_Playlist(self):
        playlist_link = self.lineEdit_6.text()
        videos_links = pafy.get_playlist(playlist_link)
        videos_items = videos_links['items']
        quality_list = []
        extensions_list = []
        for video in videos_items:
            video_data = video['pafy']
            video_link = video_data.watchv_url
            data = pafy.new(video_link)
            st = data.allstreams
            for s in st:
                size = humanize.naturalsize(s.get_filesize())
                extension_quality = s.extension + s.quality
                if extension_quality not in extensions_list:
                    data = f'Format: {s.mediatype} - Extension: {s.extension} - Quality: {s.quality} - Size: {size}'
                    quality_list.append(data)
                    extensions_list.append(extension_quality)
                else:
                    pass

        for value in quality_list:
            self.comboBox_2.addItem(value)


    def Download_Youtube_Video(self):
        video_link = self.lineEdit_3.text()
        save_location = self.lineEdit_4.text()
        v = pafy.new(video_link)
        st = v.allstreams
        quality = self.comboBox.currentIndex()
        down = st[quality].download(filepath=save_location)
        QApplication.processEvents()  # Not responding
        QMessageBox.information(self, 'Download Complete!', 'The Video Download Finished!')

    def Playlist_Download(self):
        playlist_url = self.lineEdit_6.text()
        save_location = self.lineEdit_5.text()
        playlist = pafy.get_playlist(playlist_url)
        videos = playlist['items']
        os.chdir(save_location)
        QApplication.processEvents()  # Not responding
        if os.path.exists(str(playlist['title'])):
            location = os.chdir(str(playlist['title']))
        else:
            os.mkdir(str(playlist['title']))
            location = os.chdir(str(playlist['title']))

        for video in videos:
            video_data = video['pafy']
            video_link = video_data.watchv_url
            data = pafy.new(video_link)
            st = data.allstreams
            quality = self.comboBox_2.currentIndex()
            titulo = str(video_data.title)
            self.lineEdit_7.setText(titulo)
            QApplication.processEvents()  # Not responding
            down = st[quality].download(filepath=location)
            QApplication.processEvents()  # Not responding

        QMessageBox.information(self, 'Download Complete!', 'The Videos Download Finished!')


def main():
    app = QApplication(sys.argv)
    window = MainApp()
    window.show()
    app.exec_()


if __name__ == '__main__':
    main()