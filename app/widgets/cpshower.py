from functools import partial
import sys, os
import time 

from PyQt5.QtWidgets import (
    QApplication, 
    QWidget, 
    QGridLayout, 
    QPushButton,
    QDialog,
    QApplication, 
    QWidget, 
    QGridLayout, 
    QMainWindow, 
    QPushButton, 
    QVBoxLayout,
    QTabWidget,
    QHBoxLayout,
    QDialog,
    QStyle,
    QAction,
    qApp,
    QMenu,
    QLabel,
    QToolBar,
    QToolButton,
    QTextEdit,
    QTabBar,
    QSystemTrayIcon,
    QGraphicsColorizeEffect,
)
from PyQt5.QtGui import (
    QPalette, 
    QColor, 
    QPixmap,    
    QTransform,
    QFont,
    QIcon,
    QPainter,
)

from PyQt5.QtCore import (
    QSize,
    Qt,
    QThread,
    pyqtSlot,
    pyqtSignal,
    QMetaObject,
    Q_ARG,
)

from layouts import cpManager
# from widgets.cpselecter import ListenThread


class KeyboardWidget(QWidget):
    def __init__(self, cpVID, cpPID):
        super().__init__()
        # Chemin d'accès
        self.path = os.path.dirname(os.path.realpath(__file__))
        self.path = os.path.abspath(self.path + "/../")
        self.imgs_path = os.path.join(self.path, "static", "imgs")
        # Layouts
        self.layout = QGridLayout()
        self.setLayout(self.layout)
        self.MAPPING = cpManager.get_cp_map(cpVID, cpPID)
        self.create_keys()
        self.setFixedSize(500, 500)


    def create_keys(self):
        self.keys_list = list()
        for key, value in self.MAPPING.items():
            button = KeyButton(value)
            button.clicked.connect(partial(self.show_dialog, button))
            y, x = value['position']
            self.layout.addWidget(button, x, y, 1, value['lenght'])
            self.keys_list.append(button)

    def get_keys_list(self):
        return self.keys_list

    def show_dialog(self, button):
        dialog = QDialog(self)
        dialog.setWindowTitle("Key pressed")
        layout = QVBoxLayout(dialog)
        label = QLabel(f"You pressed a key! ({button.key_name})")
        layout.addWidget(label)
        ok_button = QPushButton("OK")
        ok_button.clicked.connect(dialog.accept)
        layout.addWidget(ok_button)
        dialog.exec_()


class KeyButton(QPushButton):

    def __init__(self, value, parent=None):
        super().__init__(parent)
        # Chemin d'accès
        self.path = os.path.dirname(os.path.realpath(__file__))
        self.path = os.path.abspath(self.path + "/../")
        self.imgs_path = os.path.join(self.path, "static", "imgs")

        self.id = value['name']
        self.lenght = value['lenght']

        self.key_name = value['name']
        self.y, self.x = value['position']
        self.setAutoFillBackground(False)
        self.setStyleSheet('background:transparent; display:flex;')

        pixmap = QPixmap(os.path.join(self.imgs_path,"key.png"))
        if self.lenght > 1:
            pixmap = QPixmap(os.path.join(self.imgs_path,"key2.png"))
        self.setIconSize(QSize(50*value['lenght'], 50))

        # Créer un objet QPainter pour dessiner sur l'image
        painter = QPainter(pixmap)

        # Définir les propriétés du texte (couleur, police, etc.)
        painter.setPen(Qt.black)
        painter.setFont(QFont("Aria", 42))

        # Ajouter le texte à l'image
        text = value['name']
        painter.drawText(pixmap.rect(), Qt.AlignCenter, text)

        # Appliquer les modifications
        painter.end()
        transformed_pixmap = pixmap
        self.setIcon(QIcon(transformed_pixmap))
        
    def on_key_pressed(self):
        self.thread = HighlightThread(self)
        self.thread.start()


class HighlightThread(QThread):
    def __init__(self, key):
        super().__init__()
        self.key = key
        self.path = os.path.dirname(os.path.realpath(__file__))
        self.path = os.path.abspath(self.path + "/../")
        self.imgs_path = os.path.join(self.path, "static", "imgs")
        self.img_path = os.path.join(self.imgs_path,"key.png")
        if self.key.lenght > 1:
            self.img_path = os.path.join(self.imgs_path,"key2.png")

    def run(self):
        self.set_pressed_color()
        time.sleep(1)
        self.set_default_color()

    def set_default_color(self):
        # Créer un effet de filtre de saturation de couleur
        colorize_effect = QGraphicsColorizeEffect()
        colorize_effect.setColor(QColor("black"))

        # Appliquer l'effet au bouton
        self.key.setGraphicsEffect(colorize_effect)
    def set_pressed_color(self):
        # Créer un effet de filtre de saturation de couleur
        colorize_effect = QGraphicsColorizeEffect()
        colorize_effect.setColor(QColor("red"))

        # Appliquer l'effet au bouton
        self.key.setGraphicsEffect(colorize_effect)