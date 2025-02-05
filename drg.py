import shutil
import subprocess
from PyQt5.QtWidgets import (QFileSystemModel, QApplication, QMainWindow, QLabel, QWidget, QVBoxLayout, QPushButton, QHBoxLayout, QSizePolicy, QFileDialog)
from PyQt5.QtCore import QDir, Qt
from PyQt5.QtGui import QFont, QPixmap
from PIL import Image
import os

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle('*_^')
        self.setAcceptDrops(True)
        self.filename = None
        self.setFixedSize(600, 600)

        main_layout = QVBoxLayout()

       
        self.label_drag_drop = QLabel('Drag & Drop GIF:', self)
        self.label_drag_drop.setAlignment(Qt.AlignHCenter | Qt.AlignVCenter)
        self.label_drag_drop.setFont(QFont('Berlin Sans FB Demi', 20))
        self.label_drag_drop.setFixedHeight(50)

      
        self.label_file = QLabel(self)
        self.label_file.setAlignment(Qt.AlignCenter)
        self.label_file.setMinimumHeight(300)
        self.label_file.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)

       
        self.plus_button = QPushButton('+', self)
        self.plus_button.setFont(QFont('Arial', 50))
        self.plus_button.setStyleSheet("color: black; background-color: transparent; border: none;")  

     
        self.convert_button = QPushButton('Конвертировать', self)
        self.convert_button.setFont(QFont('Berlin Sans FB Demi', 12))
        self.convert_button.clicked.connect(lambda: op_g(self.filename))
        self.convert_button.setStyleSheet("background-color: lightgreen;")

        self.delete_button = QPushButton('Удалить', self)
        self.delete_button.clicked.connect(self.remove_file)
        self.delete_button.setFont(QFont('Berlin Sans FB Demi', 12))
        self.delete_button.setStyleSheet("background-color: lightcoral;")

        self.folder_button = QPushButton('Папка', self)
        self.folder_button.clicked.connect(self.folder)
        self.folder_button.setFont(QFont('Berlin Sans FB Demi', 12))
        self.folder_button.setStyleSheet("background-color: lightblue;")

        buttons_layout = QHBoxLayout()
        buttons_layout.addWidget(self.convert_button)
        buttons_layout.addWidget(self.delete_button)
        buttons_layout.addWidget(self.folder_button)

       
        main_layout.addWidget(self.label_drag_drop)
        main_layout.addWidget(self.label_file)
        main_layout.addWidget(self.plus_button) 
        main_layout.addLayout(buttons_layout)

        central_widget = QWidget()
        central_widget.setLayout(main_layout)
        self.setCentralWidget(central_widget)

        self._update_states()

    def _update_states(self):
        if self.label_file.pixmap() is not None:
            self.convert_button.setVisible(True)
            self.delete_button.setVisible(True)
            self.folder_button.setVisible(True)
        else:
            self.convert_button.setVisible(False)
            self.delete_button.setVisible(False)
            self.folder_button.setVisible(False)

    def open_file_dialog(self):
        options = QFileDialog.Options()
        file_name, _ = QFileDialog.getOpenFileName(self, "Выберите GIF-файл", "", "GIF Files (*.gif);;All Files (*)", options=options)
        if file_name:
            self.filename = file_name
            pixmap = QPixmap(self.filename)
            self.label_file.setScaledContents(True)
            self.label_file.setPixmap(pixmap)
            self._update_states()
            self.label_drag_drop.hide() 
            self.plus_button.hide()  
            self.setStyleSheet("")  

    def remove_file(self):
        self.label_file.clear()
        self.plus_button.show() 
        self._update_states()
        folder_path = '/Users/user/Downloads/gifConverter-main/GifResult'
        for filename in os.listdir(folder_path):
            file_path = os.path.join(folder_path, filename)
            try:
                if os.path.isfile(file_path) or os.path.islink(file_path):
                    os.unlink(file_path)
                elif os.path.isdir(file_path):
                    shutil.rmtree(file_path)
            except Exception as e:
                print(f'Failed to delete {file_path}. Why?: {e}')

    def folder(self):
        folder_path = '/Users/user/Downloads/gifConverter-main/GifResult'
        subprocess.run(['open', folder_path])  

    def dragEnterEvent(self, event):
        mime = event.mimeData()
        if mime.hasUrls():
            event.acceptProposedAction()
            self.setStyleSheet("background-color: lightgray;")  
            self.label_drag_drop.hide()
            self.plus_button.hide() 
        else:
            self.setStyleSheet("background-color: white;")

    def dropEvent(self, event):
        url = event.mimeData().urls()[0]
        self.filename = url.toLocalFile()
        pixmap = QPixmap(self.filename)
        self.label_file.setScaledContents(True)
        self.label_file.setPixmap(pixmap)
        self._update_states()
        self.label_drag_drop.show()
        self.plus_button.hide()  
        self.setStyleSheet("")
        return super().dropEvent(event)

def op_g(filename):
    with Image.open(filename) as im:
        im.seek(0)
        i = 0
        try:
            while True:
                im.seek(im.tell() + 1)
                i += 1
                im.save("/Users/user/Downloads/gifConverter-main/GifResult/{}.png".format(i))
        except EOFError:
            pass

if __name__ == '__main__':
    import sys
    app = QApplication(sys.argv)

    w = MainWindow()
    w.show()
    sys.exit(app.exec_())
