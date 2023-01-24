# ControlPads Viewer

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

from core.cpgetter import get_dict_products
from core.listener import listen_usb


class CPViewerWidget(QWidget):
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

        # Mise en place de l'interface utilisateur
        self.setLayout(QVBoxLayout())
        self.devices_groupbox = QGroupBox("Devices Available")
        self.devices_layout = QVBoxLayout()
        self.devices_groupbox.setLayout(self.devices_layout)

        products_list = list()
        for IDs, info in get_dict_products().items():
            product_widget = QWidget()
            product_widget.setLayout(QHBoxLayout())
            # Label
            product = info.get("product")
            manufacturer = info.get("manufacturer")
            product_label = QLabel(f"[{manufacturer}] - {product}")
            product_widget.id = int(f"{IDs[0]}{IDs[1]:04}")
            product_widget.idVendor  = IDs[0]
            product_widget.idProduct = IDs[1]
            product_widget.button = QPushButton("Select")

            # Display
            product_widget.layout().addWidget(product_label)
            product_widget.layout().addWidget(product_widget.button)
            # Add to list
            products_list.append(product_widget)
            self.devices_layout.addWidget(product_widget)
        # Bouton Enregistrer
        self.save_button = QPushButton("Save")
        # Bouton Par Défaut
        self.default_button = QPushButton("Default")

        # sublayout
        sublayout_1 = QHBoxLayout()
        sublayout_1.addWidget(self.devices_groupbox)
        self.layout().addLayout(sublayout_1)
        
        # save / default
        self.layout().addWidget(self.save_button)
        self.layout().addWidget(self.default_button)

        self.save_button.clicked.connect(self.save_settings)
        self.default_button.clicked.connect(self.default_settings)

        for device in products_list:
            device.button.clicked.connect(partial(self.say_carac, device))

    def say_carac(self, dev):
        listen_usb(idVendor=dev.idVendor, idProduct=dev.idProduct)

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
