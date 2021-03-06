from PySide2.QtCore import Qt
from PySide2.QtGui import QGuiApplication
from PySide2.QtWidgets import QMessageBox, QStyle


class PopupWindow(QMessageBox):
    def __init__(self, parent, text, window_type):
        super(PopupWindow, self).__init__()

        # Set window center of screen
        self.setGeometry(
            QStyle.alignedRect(
                Qt.LeftToRight,
                Qt.AlignCenter,
                self.size(),
                QGuiApplication.primaryScreen().availableGeometry(),
            ),
        )

        title = "Álláskereső"

        if window_type == "information":
            self.information(parent, title, text)
        elif window_type == "warning":
            self.warning(parent, title, text)
