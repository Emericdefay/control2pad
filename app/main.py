import sys, os
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
)
from PyQt5.QtGui import (
    QPalette, 
    QColor, 
    QFont,
    QIcon,
)

from PyQt5.QtCore import (
    QSize,
    Qt,
    pyqtSlot,
    pyqtSignal,
)

from widgets.cpselecter import CPHandler


class MainWindow(QMainWindow):

    def __init__(self):
        super().__init__()
        self.setWindowFlag(Qt.WindowMaximizeButtonHint, False)
        self.initUI()
        self.startUI()
        self.trayUI()


    def initUI(self):
        # définissez la largeur et la hauteur de la fenêtre
        self.setGeometry(100, 100, 600, 600)
        self.max_height = 580

        # Charger l'icône à partir d'un fichier
        self.setWindowIcon(QIcon(':/icons/favicon'))

        # définissez le titre de la fenêtre
        self.setWindowTitle("ControlSquarePad")

        # définissez la couleur de fond de la fenêtre
        palette = QPalette()
        palette.setColor(QPalette.Background, QColor(76, 112, 140))
        self.setPalette(palette)

        # Chemin d'accès
        self.path = os.path.dirname(os.path.realpath(__file__))
        self.imgs_path = os.path.join(self.path, "static", "imgs")

    def startUI(self):
        # Création du QTabWidget
        self.tabs = QTabWidget()
        self.tabs.tabBar().setMovable(True)
        self.central_widget = QWidget()
        self.setCentralWidget(self.central_widget)
        main_layout = QVBoxLayout()
        main_layout.addWidget(self.tabs)
        self.central_widget.setLayout(main_layout)
        self.setWindowIcon(QIcon("icon.png"))

        # Ajout d'un bouton pour ajouter des onglets
        add_tab_button = QToolButton()
        add_tab_button.setIcon(QIcon(os.path.join(self.imgs_path,"plus.png")))
        add_tab_button.clicked.connect(self.add_tab)
        self.tabs.setCornerWidget(add_tab_button, corner=Qt.TopRightCorner)

        self.add_tab()

    def trayUI(self):
        self.tray_icon = QSystemTrayIcon(self)
        self.tray_icon.setIcon(self.style().standardIcon(QStyle.SP_ComputerIcon))

        show_action = QAction("Show", self)
        quit_action = QAction("Exit", self)
        hide_action = QAction("Hide", self)
        show_action.triggered.connect(self.show)
        hide_action.triggered.connect(self.hide)
        quit_action.triggered.connect(qApp.quit)
        tray_menu = QMenu()
        tray_menu.addAction(show_action)
        tray_menu.addAction(hide_action)
        tray_menu.addAction(quit_action)
        self.tray_icon.setContextMenu(tray_menu)
        self.tray_icon.show()

        self.tray_icon.activated.connect(self.tray_double_clicked)


    @pyqtSlot()
    def close_cpviewer_widget(self):
        """Ferme la fenêtre modale des paramètres."""
        self.cpviewer_dialog.hide()

    def tray_double_clicked(self, reason):
        if reason == QSystemTrayIcon.DoubleClick:
            self.show()
            self.showNormal()

    def add_tab(self):
        # new_tab = QPushButton("Select your ControlPad")
        # new_tab.clicked.connect(self.show_cpviewer_widget)
        new_tab = CPHandler()

        close_button = QToolButton()
        close_button.setIcon(QIcon(os.path.join(self.imgs_path, "cross.png")))
        close_button.setAutoFillBackground(False)
        close_button.setStyleSheet("background:transparent; margin-top: 1px;")
        self.tabs.addTab(new_tab, "Onglet " + str(self.tabs.count()+1))
        self.tabs.tabBar().setTabButton(self.tabs.count()-1, QTabBar.RightSide, close_button)
        close_button.clicked.connect(lambda: self.remove_tab(new_tab))

    def remove_tab(self, tab: CPHandler):
        nb_tabs = self.tabs.count()
        index = self.tabs.indexOf(tab)
        if nb_tabs > 1:
            try:
                # product available again
                CPHandler.products_handled.remove((tab.idVendor, tab.idProduct))

            except ValueError as e:
                pass
            # close threads
            tab.closeWidget()
            # remove tab
            self.tabs.removeTab(index)
            
    def closeEvent(self, event):
        if self.isMinimized():
            self.hide()
            event.ignore()
    
    def changeEvent(self, event):
        if self.isMinimized():
            self.hide()
            event.ignore()
            self.tray_icon.showMessage(
                "Tray Program",
                "Control2Pad was minimized to Tray",
                QSystemTrayIcon.Information,
                2000
            )

    @pyqtSlot(QSystemTrayIcon.ActivationReason)
    def on_systemTrayIcon_activated(self, reason):
        if reason == QSystemTrayIcon.DoubleClick:
            if self.isHidden():
                self.show()
            else:
                self.hide()

    def resizeEvent(self, event) -> None:
        super().resizeEvent(event)
        return 


if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())
