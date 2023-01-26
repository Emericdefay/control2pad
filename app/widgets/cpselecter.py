from PyQt5.QtWidgets import (
    QWidget, 
    QListWidget,
    QPushButton, 
    QVBoxLayout,
    QHBoxLayout,
    QDialog,
    QListWidgetItem,
)
from PyQt5.QtGui import (
    QPalette, 
    QColor, 
)

from PyQt5.QtCore import (
    Qt,
    QThread,
)

from core.cpgetter import get_dict_products
from core.listener import listen_usb
from widgets.cpshower import KeyboardWidget


class CPHandler(QWidget):

    products_handled = list()

    def __init__(self):
        super().__init__()
        self.layout = QHBoxLayout(self)
        self.setLayout(self.layout)

        self.setAutoFillBackground(True)
        palette = QPalette()
        palette.setColor(QPalette.Background, QColor(97, 122, 153))
        self.setPalette(palette)

        self.button = QPushButton("Choose device")
        self.button.setStyleSheet('max-width:100px;')
        self.button.clicked.connect(self.show_dialog)
        self.layout.addWidget(self.button)
        self.products_list = list()
        self.cp_selected = None
        self.idVendor = None
        self.idProduct = None
        
    def closeWidget(self):
        try:
            self.cpshower.stopped = True
            self.thread.close()
        except AttributeError:
            pass

    def show_dialog(self):
        dialog = QDialog()
        dialog.setWindowTitle("Choose device")
        layout = QVBoxLayout(dialog)

        self.generate_list()

        # Ajout des options de mode dans la liste
        cp_list = QListWidget()
        for item in self.products_list:
            obj = QListWidgetItem()

            kwargs = {
                'label': item.label,
                'idVendor': item.idVendor,
                'idProduct': item.idProduct,
            }

            obj.setText(item.label)
            obj.setData(Qt.UserRole, kwargs)
            if (item.idVendor, item.idProduct) not in CPHandler.products_handled:
                cp_list.addItem(obj)
        # Ajout de la liste au layout du QDialog
        layout.addWidget(cp_list)

        # Ajout d'un bouton OK
        ok_button = QPushButton("OK")
        ok_button.clicked.connect(dialog.accept)
        layout.addWidget(ok_button)

        result = dialog.exec_()
        if result == QDialog.Accepted:
            # Récupération de l'item sélectionné
            selected_item = cp_list.currentItem()
            if selected_item is not None:
                selected_cp = selected_item
                self.handle_cp(selected_cp)

    def handle_cp(self, mode):
        # Suppression du bouton
        self.button.hide()
        self.button.deleteLater()
        if mode is not None and\
           self.cp_selected is None:
            # retrieve data
            self.cp_selected = mode
            data = mode.data(Qt.UserRole)
            idVendor = data.get('idVendor')
            idProduct = data.get('idProduct')
            self.idVendor = idVendor
            self.idProduct = idProduct
            CPHandler.products_handled.append((idVendor, idProduct))
            # Draw map
            self.cpshower = KeyboardWidget(idVendor, idProduct)
            print(self.cpshower)
            self.layout.addWidget(self.cpshower)
            # listen in another thread
            self.thread = ListenThread(idVendor, idProduct, self.cpshower)
            self.thread.start()

    def generate_list(self):
        self.products_list = list()
        for IDs, info in get_dict_products().items():
            product_widget = QWidget()
            # Label
            product = info.get("product")
            manufacturer = info.get("manufacturer")
            product_widget.id = int(f"{IDs[0]}{IDs[1]:04}")
            product_widget.idVendor  = IDs[0]
            product_widget.idProduct = IDs[1]
            product_widget.label = f"[{manufacturer}] - {product}"

            # Add to list
            self.products_list.append(product_widget)


class ListenThread(QThread):

    def __init__(self, idVendor, idProduct, keyboard_map):
        super().__init__()
        self.idVendor = idVendor
        self.idProduct = idProduct
        self.keyboard_map = keyboard_map

    def run(self):
        listen_usb(self.idVendor, self.idProduct, self.keyboard_map)
        
    def close(self):
        self.quit()
