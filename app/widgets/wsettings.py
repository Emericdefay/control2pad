import json
from functools import partial
from PyQt5.QtWidgets import (
    QWidget,
    QPushButton, 
    QLabel,
    QVBoxLayout, 
    QGroupBox, 
    QHBoxLayout,
    QColorDialog,
    QGraphicsDropShadowEffect,
)
from PyQt5.QtGui import (
    QColor,
    QFont,
    QPalette,
)
from PyQt5.QtCore import (
    pyqtSignal,
    Qt,
)

from settings.json_settings import load_settings, write_default_json


class SettingsWidget(QWidget):
    """Widget permettant de changer les paramètres de l'application.

    Attributes:
        parent (QWidget): Widget parent.
        settings (dict): Dictionnaire contenant les paramètres de 
                         l'application.
    """
    # Définition du signal personnalisé settingsSaved
    settingsSaved = pyqtSignal()

    def __init__(self, parent=None):
        super().__init__(parent)

        # Charge les paramètres
        self.settings = load_settings()

        palette = QPalette()
        palette.setColor(QPalette.Background, QColor(129, 129, 129))
        self.setPalette(palette)

       
        # Bouton Enregistrer
        self.save_button = QPushButton("Enregistrer")
        # Bouton Par Défaut
        self.default_button = QPushButton("Défaut")

        # save / default
        self.layout().addWidget(self.save_button)
        self.layout().addWidget(self.default_button)

        self.save_button.clicked.connect(self.save_settings)
        self.default_button.clicked.connect(self.default_settings)

    def save_settings(self):
        """Sauvegarde les paramètres de l'application dans un fichier JSON.

        Returns:
            bool: True si les paramètres ont été sauvegardés avec succès, 
            False sinon.
        """
        try:
            with open('settings.json', 'w') as f:
                json.dump(self.settings, f)
        except Exception as e:
            print(e)
            return False
        # Emettre le signal settingsSaved
        self.settingsSaved.emit()
        # Fermer la fenêtre
        self.close()
        return True

    def default_settings(self):
        with open("settings.json", "w") as f:
            json.dump(write_default_json(), f, indent=4)
        with open("settings.json", "r") as f:
            self.settings = json.load(f)
        # Emettre le signal settingsSaved
        self.settingsSaved.emit()
        # Fermer la fenêtre
        self.close()
