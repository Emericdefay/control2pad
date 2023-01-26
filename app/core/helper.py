import sys
import json

from PyQt5.QtWidgets import (
    QApplication, 
    QWidget, QTableWidget,QTableWidgetItem,
    QMainWindow, 
    QVBoxLayout,
)
from PyQt5.QtGui import (
    QIcon,
)
from PyQt5.QtCore import (
    QTimer,
)


class MyWindow(QWidget):

    def __init__(self, cp_path):
        super().__init__()
        self.cp_path = cp_path
        self.data = self.load_config()
        self.initUI()

    def initUI(self):

        layout = QVBoxLayout(self)

        self.table = QTableWidget(len(self.data), 3)
        self.table.setHorizontalHeaderLabels(["Key", "Type", "Value"])

        for i, (key, value) in enumerate(self.data.items()):
            self.table.setItem(i, 0, QTableWidgetItem(key))
            self.table.setItem(i, 1, QTableWidgetItem(str(value['type'])))
            self.table.setItem(i, 2, QTableWidgetItem(str(value['value'])))
        self.table.resizeColumnsToContents()
        layout.addWidget(self.table)

    def load_config(self):
        try:
            with open(self.cp_path, 'r') as f:
                config = json.load(f)
            config = dict(sorted(config.items()))
            return config
        except FileNotFoundError:
            pass


class HelperMainWindow(QMainWindow):

    def __init__(self, cp_path):
        super().__init__()
        self.timer = QTimer()
        self.timer.setInterval(10000)
        self.timer.setSingleShot(True)
        self.timer.timeout.connect(self.close)
        self.cp_path = cp_path
        self.startUI()
        self.initUI()

        horizontal = self.widget.table.horizontalHeader()
        vertical = self.widget.table.verticalHeader()
        frame = self.widget.table.frameWidth() * 2
        cst = 30
        x = horizontal.length() + vertical.sizeHint().width() + frame + cst
        y = vertical.length() + horizontal.sizeHint().height() + frame + cst

        self.setGeometry(100, 100, x, y)

    def initUI(self):
        # Charger l'icône à partir d'un fichier
        self.setWindowIcon(QIcon(':/icons/favicon'))

        # définissez le titre de la fenêtre
        self.setWindowTitle("ControlSquarePad")

    def startUI(self):
        # Création du QTabWidget
        self.widget = MyWindow(self.cp_path)
        self.setCentralWidget(self.widget)
        self.timer.start()

    def close(self):
        sys.exit(helper_app.exec_())


if __name__ == '__main__':
    helper_app = QApplication(sys.argv)
    helper = HelperMainWindow(sys.argv[1])
    helper.show()
    helper.showNormal()
    sys.exit(helper_app.exec_())
