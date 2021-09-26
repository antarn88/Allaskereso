from PySide2.QtCore import Qt
from PySide2.QtWidgets import QWidget, QGridLayout, QGroupBox, QLineEdit, QListWidget, QListWidgetItem, QPushButton, QComboBox, QHBoxLayout

from parts.Database import Database
from parts.InputData import InputData
from parts.PortalManager import PortalManager
from utilities.PopupWindow import PopupWindow

db = Database()


class SettingsTab(QWidget):
    def __init__(self, parent):
        super(SettingsTab, self).__init__()

        # App attributes
        self.portal_manager = None
        self.portal_items = []
        self.selected_portals = []

        self.parent = parent

        main_layout = QGridLayout()
        self.setLayout(main_layout)

        self.keywords_box = QGroupBox("Keresési kulcsszavak (vesszővel elválasztva):")
        main_layout.addWidget(self.keywords_box, 0, 0)
        keywords_box_layout = QGridLayout()
        keywords_box_layout.setContentsMargins(50, 10, 50, 10)
        keywords_box_layout.setHorizontalSpacing(30)
        self.keywords_box.setLayout(keywords_box_layout)
        self.keywords_input = QLineEdit()
        self.keywords_input.returnPressed.connect(self.search_jobs_action)

        self.keywords_input.setText(db.get_searched_jobs_from_db_str())
        self.keywords_input.setToolTip("Ha üresen hagyod, az összes állás megjelenik")
        keywords_box_layout.addWidget(self.keywords_input)

        self.exclude_words_box = QGroupBox("Kulcsszavak kizárása (vesszővel elválasztva):")
        main_layout.addWidget(self.exclude_words_box, 1, 0)
        exclude_words_box_layout = QGridLayout()
        exclude_words_box_layout.setContentsMargins(50, 10, 50, 10)
        exclude_words_box_layout.setHorizontalSpacing(30)
        self.exclude_words_box.setLayout(exclude_words_box_layout)
        self.exclude_words_input = QLineEdit()
        self.exclude_words_input.returnPressed.connect(self.search_jobs_action)

        self.exclude_words_input.setText(db.get_exclude_words_from_db_str())
        exclude_words_box_layout.addWidget(self.exclude_words_input)

        self.job_locations_box = QGroupBox("Állások keresése innen:")
        main_layout.addWidget(self.job_locations_box, 2, 0)
        job_locations_box_layout = QGridLayout()
        job_locations_box_layout.setContentsMargins(50, 10, 50, 10)
        job_locations_box_layout.setHorizontalSpacing(30)
        self.job_locations_box.setLayout(job_locations_box_layout)

        self.location_list = QComboBox()
        [self.location_list.addItem(location) for location in db.get_locations()]

        job_locations_box_layout.addWidget(self.location_list)
        self.location_list.setCurrentText(db.get_location())

        self.job_search_portals_box = QGroupBox("Álláskeresési portálok:")
        main_layout.addWidget(self.job_search_portals_box, 3, 0)
        job_search_portals_box_layout = QGridLayout()
        job_search_portals_box_layout.setContentsMargins(50, 10, 50, 10)
        job_search_portals_box_layout.setHorizontalSpacing(30)
        self.job_search_portals_box.setLayout(job_search_portals_box_layout)
        self.portals_list = QListWidget()
        self.portals_list.itemChanged.connect(self.select_deselect_all_item)
        self.portals_list.itemPressed.connect(self.select_deselect_item)
        job_search_portals_box_layout.addWidget(self.portals_list)

        for portal in db.get_supported_portals():
            portal_item = PortalItem(portal)
            self.portal_items.append(portal_item)
            self.portals_list.addItem(portal_item)

        button_group = QHBoxLayout()
        self.save_and_recommended_jobs_btn = QPushButton("Állások keresése")
        self.save_and_recommended_jobs_btn.clicked.connect(self.search_jobs_action)

        button_group.addWidget(self.save_and_recommended_jobs_btn)
        main_layout.addLayout(button_group, 4, 0)

    def search_jobs_action(self):
        if self.parent.has_internet_connection():
            self.parent.abort_all_running_threads()
            self.selected_portals.clear()
            for portal_item in self.portal_items:
                if portal_item.checkState():
                    self.selected_portals.append(portal_item.text())
            db.set_portals(self.selected_portals)
            processed_data = InputData(
                self.keywords_input.text(),
                self.exclude_words_input.text(),
                self.location_list.currentText(),
                self.selected_portals
            ).get_processed_data()
            self.portal_manager = PortalManager(self, processed_data)
        else:
            PopupWindow(self, "Nincs internet kapcsolat!", "warning")

    def select_deselect_item(self, item):
        item.setCheckState(Qt.Unchecked) if item.checkState() else item.setCheckState(Qt.Checked)

    def select_deselect_all_item(self, item):
        if item.text() == "Mindegyik/egyik sem":
            if item.checkState():
                for portal_item in self.portal_items:
                    portal_item.setCheckState(Qt.Checked)
            else:
                for portal_item in self.portal_items:
                    portal_item.setCheckState(Qt.Unchecked)


class PortalItem(QListWidgetItem):
    def __init__(self, portal_name):
        super().__init__()
        self.portal_name = portal_name
        self.setText(self.portal_name)
        self.first_running = not db.get_portals()

        if self.first_running:
            if portal_name == "Mindegyik/egyik sem" or \
                    portal_name == "Közigállás (kozigallas.gov.hu)" or \
                    portal_name == "Borsodchem (karrier.borsodchem.eu)":
                self.setCheckState(Qt.Unchecked)
            else:
                self.setCheckState(Qt.Checked)
        else:
            if self.portal_name in db.get_portals():
                self.setCheckState(Qt.Checked)
            else:
                self.setCheckState(Qt.Unchecked)
