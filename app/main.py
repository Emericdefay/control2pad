import sys
from PyQt5.QtWidgets import (
    QApplication, 
    QWidget, 
    QGridLayout, 
    QMainWindow, 
    QPushButton, 
    QVBoxLayout,
    QTabWidget,
    QHBoxLayout,
    QDialog,
    QLabel,
    QTextEdit,
    
)
from PyQt5.QtGui import (
    QPalette, 
    QColor, 
    QFont,
    QIcon,
)

from PyQt5.QtCore import (
    Qt,
    pyqtSlot,
    pyqtSignal,
)


from widgets.cpviewer import CPViewerWidget

class MainWindow(QWidget):

    def __init__(self):
        super().__init__()
        self.setWindowFlag(Qt.WindowMaximizeButtonHint, False)
        self.initUI()
        self.startUI()

    def initUI(self):
        # définissez la largeur et la hauteur de la fenêtre
        self.setGeometry(100, 100, 1200, 610)
        self.max_height = 580

        # Charger l'icône à partir d'un fichier
        self.setWindowIcon(QIcon(':/icons/favicon'))

        # définissez le titre de la fenêtre
        self.setWindowTitle("ControlSquarePad")

        # définissez la couleur de fond de la fenêtre
        palette = QPalette()
        palette.setColor(QPalette.Background, QColor(76, 112, 140))
        self.setPalette(palette)

    def startUI(self):
        # créez des layouts et ajoutez des widgets à partir de vos modules
        layout = QGridLayout(self)
        self.setLayout(layout)

        # Créez une instance de QTabWidget et ajoutez-la au layout principal de votre fenêtre
        self.tab_widget = QTabWidget(self)
        self.tab_widget.tabCloseRequested.connect(lambda index: self.tab_widget.removeTab(index))

        self.parameters = QPushButton("ControlPads Viewer")
        self.parameters.clicked.connect(self.show_cpviewer_widget)

        self.layout().addWidget(self.parameters)

        

    def show_cpviewer_widget(self):
        # Création de la fenêtre modale
        self.cpviewer_dialog = QDialog(self)
        # Création de l'instance de SettingsWidget
        self.cpviewer_widget = CPViewerWidget()
        # Ajout de SettingsWidget à la fenêtre modale en utilisant un layout
        self.cpviewer_dialog.setLayout(QVBoxLayout())
        self.cpviewer_dialog.layout().addWidget(self.cpviewer_widget)
        # Connexion du signal settingsSaved à la slot close_cpviewer_widget
        self.cpviewer_widget.settingsSaved.connect(self.close_cpviewer_widget)
        # Affichage de la fenêtre modale
        self.cpviewer_dialog.exec_()

    @pyqtSlot()
    def close_cpviewer_widget(self):
        """Ferme la fenêtre modale des paramètres."""
        self.cpviewer_dialog.hide()


    def resizeEvent(self, event) -> None:
        super().resizeEvent(event)
        return 


if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())
