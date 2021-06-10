from PySide2.QtCore import Qt
from PySide2.QtWidgets import QWidget, QGridLayout, QListWidget, QProgressBar, QPushButton


class JobsTab(QWidget):
    def __init__(self, parent):
        super(JobsTab, self).__init__()

        main_layout = QGridLayout()
        self.setLayout(main_layout)

        self.output_panel = QListWidget()
        main_layout.addWidget(self.output_panel, 1, 0, 1, 2)

        self.progressbar = QProgressBar()
        self.progressbar.setAlignment(Qt.AlignCenter)
        self.progressbar.setMaximum(0)
        self.progressbar.setVisible(False)

        self.abort_btn = QPushButton("Mégse")
        self.abort_btn.clicked.connect(self.abort_action)
        self.abort_btn.setVisible(False)

        main_layout.addWidget(self.progressbar, 2, 0)
        main_layout.addWidget(self.abort_btn, 2, 1)

        self.parent = parent
        self.abort_all_running_threads = self.parent.abort_all_running_threads

    def abort_action(self):
        self.abort_btn.setVisible(False)
        self.progressbar.setVisible(False)
        self.abort_all_running_threads()
        keywords_input = self.parent.settings_tab.keywords_input
        keywords_input.setFocus()
