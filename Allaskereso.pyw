from socket import error
from sys import argv

from PySide2.QtCore import Qt
from PySide2.QtGui import QGuiApplication, QIcon, QPixmap
from PySide2.QtWidgets import QMainWindow, QApplication, QWidget, QStyle, QGridLayout, QTabWidget
from requests import get

from parts.Database import Database
from portals.Kozigallas import KozigallasWorker
from tabs.JobsTab import JobsTab
from tabs.SettingsTab import SettingsTab
from utilities.GetImages import app_icon


class Allaskereso(QMainWindow):
    def __init__(self):
        super(Allaskereso, self).__init__()

        # The size of the starting window
        self.resize(865, 600)

        # Set window center of screen
        self.setGeometry(
            QStyle.alignedRect(
                Qt.LeftToRight,
                Qt.AlignCenter,
                self.size(),
                QGuiApplication.primaryScreen().availableGeometry(),
            ),
        )

        self.setWindowIcon(QIcon(QPixmap(app_icon())))

        # The version of the program
        self.version = "v1.26"

        # The title of the program
        self.setWindowTitle(f"Álláskereső {self.version}")

        # Before using the main layout, need to create a central widget
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        main_layout = QGridLayout(central_widget)

        self.tabwidget = QTabWidget()
        self.jobs_tab = JobsTab(self)
        self.settings_tab = SettingsTab(self)
        self.tabwidget.addTab(self.settings_tab, "Keresési beállítások")
        self.tabwidget.addTab(self.jobs_tab, "Állások")
        main_layout.addWidget(self.tabwidget)

        self.settings_tab.keywords_input.setFocus()

        Database()

    def has_internet_connection(self):
        try:
            get("https://www.google.com")
        except error:
            return False
        return True

    def abort_all_running_threads(self):
        if self.settings_tab.portal_manager:
            for thread in self.settings_tab.portal_manager.threads:
                if thread.isRunning():
                    thread.terminate()
                    thread.wait()
                    if isinstance(thread, KozigallasWorker):
                        thread.driver.quit()

    def closeEvent(self, event):
        self.abort_all_running_threads()


if __name__ == '__main__':
    app = QApplication(argv)
    win = Allaskereso()
    win.show()
    app.exec_()
