from functools import partial
import sys, os
import time 
import json

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
    QLineEdit,
    QComboBox,
    QFileDialog,
)
from PyQt5.QtGui import (
    QPalette, 
    QColor, 
    QPixmap,    
    QTransform,
    QRegion,
    QFont,
    QIcon,
    QKeySequence,
    QPainter,
)

from PyQt5.QtCore import (
    QSize,
    QTimer,
    Qt,
    QThread,
    pyqtSlot,
    pyqtSignal,
    QMetaObject,
    Q_ARG,
)

from layouts import cpManager
# from widgets.cpselecter import ListenThread
from settings.core_settings import OPTIONS


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
        self.cpVID = cpVID
        self.cpPID = cpPID
        self.create_keys()
        self.setFixedSize(500, 500)
        self.stopped = False
        #color if needed
        self.setAutoFillBackground(True)


    def create_keys(self):
        self.keys_list = list()
        for key, value in self.MAPPING.items():
            button = KeyButton(value, self.cpPID, self.cpVID)
            button.clicked.connect(partial(self.show_dialog, button))
            y, x = value['position']
            self.layout.addWidget(button, x, y, 1, value['lenght'])
            self.keys_list.append(button)

    def get_keys_list(self):
        return self.keys_list

    def show_dialog(self, button):
        print(button)
        dialog = KeyConfigDialog(button, self.cpPID, self.cpVID)
        dialog.exec_()


class KeyButton(QPushButton):

    def __init__(self, value, cpPID, cpVID, parent=None):
        super().__init__(parent)
        # Chemin d'accès
        self.path = os.path.dirname(os.path.realpath(__file__))
        self.path = os.path.abspath(self.path + "/../")
        self.imgs_path = os.path.join(self.path, "static", "imgs")

        self.thread = None

        self.id = value['name']
        self.lenght = value['lenght']
        self.cpPID, self.cpVID = cpPID, cpVID

        self.key_name = value['name']
        self.y, self.x = value['position']
        self.setAutoFillBackground(False)
        self.setStyleSheet('background:transparent; display:flex;')

        pixmap = QPixmap(os.path.join(self.imgs_path,"key.png"))
        if self.lenght > 1:
            pixmap = QPixmap(os.path.join(self.imgs_path,"key2.png"))
        self.setIconSize(QSize(50 * value['lenght'], 50))

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

        self.thread_2 = ExecKeyThread(self, self.cpPID, self.cpVID)
        self.thread_2.start()


class HighlightThread(QThread):
    def __init__(self, key):
        super().__init__()
        self.key = key

    def run(self):
        self.set_pressed_color()
        time.sleep(0.5)
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
        colorize_effect.setColor(QColor("white"))

        # Appliquer l'effet au bouton
        self.key.setGraphicsEffect(colorize_effect)



class KeyConfigDialog(QDialog):
    def __init__(self, key, cpPID, cpVID, parent=None):
        super().__init__(parent)
        self.json_file = f"cp_{cpPID}_{cpVID}.json"
        self.key_name = key.key_name
        self.layout = QVBoxLayout(self)
        self.setLayout(self.layout)
        self.loaded = False

        self.action_label = QLabel("Action for key '{}':".format(self.key_name))
        self.layout.addWidget(self.action_label)

        self.action_selector = QComboBox()
        actions_availables = ['---'] + list(OPTIONS.values())
        self.action_selector.addItems(actions_availables)
        self.action_selector.currentIndexChanged.connect(self.update_interface)
        self.layout.addWidget(self.action_selector)

        self.action_input = QLineEdit()
        self.action_input.installEventFilter(self)
        self.layout.addWidget(self.action_input)

        self.save_button = QPushButton("Save")
        self.save_button.clicked.connect(self.save_config)
        self.layout.addWidget(self.save_button)

        self.load_config()
        self.save_config()

    def save_config(self):
        config = {}
        try:
            with open(self.json_file, 'r') as f:
                config = json.load(f)
        except json.decoder.JSONDecodeError :
            pass
        except FileNotFoundError :
            pass
        action = self.action_selector.currentText()
        value = self.action_input.text()
        if action == OPTIONS['script']:
            config[self.key_name] = {"type": "script", "value": value}
        elif action == OPTIONS['program']:
            config[self.key_name] = {"type": "program", "value": value}
        elif action == OPTIONS['shortcut']:
            config[self.key_name] = {"type": "shortcut", "value": value}
        elif action == OPTIONS['help']:
            config[self.key_name] = {"type": "help", "value": value}
        
        with open(self.json_file, 'w') as f:
            json.dump(config, f)

        self.close()

    def update_interface(self):
        if self.loaded :
            action = self.action_selector.currentText()
            if action == OPTIONS['script']:
                self.action_input.setReadOnly(False)
                self.action_input.setPlaceholderText("Enter path to script")
                self.action_input.setToolTip("Enter path to script")
                self.action_input.setText("")
                # self.action_input.returnPressed.connect(self.open_file_dialog)
                file_name = self.open_file_dialog()
                if file_name:
                    self.action_input.setText(file_name)
            elif action == OPTIONS['program']:
                self.action_input.setReadOnly(False)
                self.action_input.setPlaceholderText("Enter path to program")
                self.action_input.setToolTip("Enter path to program")
                self.action_input.setText("")
                # self.action_input.returnPressed.connect(self.open_file_dialog)
                file_name = self.open_file_dialog()
                if file_name:
                    self.action_input.setText(file_name)
            elif action == OPTIONS['shortcut']:
                self.action_input.setReadOnly(True)
                self.action_input.setPlaceholderText("Waiting for key pressed")
                self.action_input.setFocus()
                self.action_input.keyPressEvent = self.keyPressEvent
            elif action == OPTIONS['help']:
                self.action_input.setReadOnly(True)
                self.action_input.setPlaceholderText("Helper displaying")

    def keyPressEvent(self, event):
        key = event.key()
        self.action_input.setText(QKeySequence(key).toString())
        self.action_input.setReadOnly(False)
        self.action_input.keyPressEvent = None

    def open_file_dialog(self):
        current_action = self.action_selector.currentText()
        if current_action == OPTIONS['script']:
            options = QFileDialog.Options()
            options |= QFileDialog.ReadOnly
            file_name, _ = QFileDialog.getOpenFileName(self,"QFileDialog.getOpenFileName()", "","Python Files (*.py);;All Files (*)", options=options)
            if file_name:
                return file_name
        elif current_action == OPTIONS['program']:
            options = QFileDialog.Options()
            options |= QFileDialog.ReadOnly
            file_name, _ = QFileDialog.getOpenFileName(self,"QFileDialog.getOpenFileName()", "","All Files (*)", options=options)
            if file_name:
                return file_name
        elif current_action == OPTIONS['shortcut']:
            self.action_input.setReadOnly(True)
            self.action_input.setText("Waiting for key pressed...")
            self.action_input.keyPressEvent = self.get_key_pressed

    def load_config(self):
        try:
            with open(self.json_file, 'r') as f:
                config = json.load(f)
                for key, value in config.items():
                    if key == self.key_name:
                        self.action_input.setText(value.get("value"))
                        self.action_selector.setCurrentText(OPTIONS[value.get("type")])
        except FileNotFoundError:
            pass
        self.loaded = True


class ExecKeyThread(QThread):

    help_dialog_open = False

    def __init__(self, key, cpPID, cpVID):
        super().__init__()
        self.key = key
        self.json_file = f"cp_{cpPID}_{cpVID}.json"
        self.ASSOCIATION = {
            "script": "Python script",
            "program": "Program launcher",
            "shortcut": "Keyboard shortcut",
        }
        self.action_input = None
        self.action_selector = None

    def run(self):
        self.load_config()
        if not self.action_input or not self.action_selector:
            print("Empty key binding")
            self.quit()
        if self.action_selector == "script":
            import subprocess
            subprocess.run(['python', self.action_input])
        elif self.action_selector == "program":
            import subprocess
            subprocess.run(['open', self.action_input])
        elif self.action_selector == "shortcut":
            import pyautogui
            if len(self.action_input)>1:
                pyautogui.typewrite(self.action_input)
            else:
                pyautogui.hotkey(self.action_input)
        elif self.action_selector == "help":
            import subprocess
            from core import helper
            subprocess.run(['python', os.path.realpath(helper.__file__), self.json_file])

    def load_config(self):
        try:
            with open(self.json_file, 'r') as f:
                config = json.load(f)
                for key, value in config.items():
                    if key == self.key.key_name:
                        self.action_input = value.get("value")
                        self.action_selector = value.get("type")
        except FileNotFoundError:
            pass
