from PySide2.QtCore import QUrl
from PySide2.QtGui import QDesktopServices, QColor
from PySide2.QtWidgets import QListWidgetItem

from portals.AllasClub import AllasClubWorker
from portals.Borsodchem import BorsodchemWorker
from portals.Bosch import BoschWorker
from portals.Cvonline import CvonlineWorker
from portals.ERV import ERVWorker
from portals.Evosoft import EvosoftWorker
from portals.Humancentrum import HumancentrumWorker
from portals.Jobmonitor import JobmonitorWorker
from portals.Kozigallas import KozigallasWorker
from portals.Pannonwork import PannonworkWorker
from portals.Profession import ProfessionWorker
from portals.VMP import VMPWorker
from utilities.PopupWindow import PopupWindow


class PortalManager:
    def __init__(self, parent, input_data):

        # App attributes
        self.found_job_counter = 0
        self.error_counter = 0
        self.number_of_active_portals = 0
        self.profession_worker = None
        self.evosoft_worker = None
        self.bosch_worker = None
        self.allas_club_worker = None
        self.vmp_worker = None
        self.jobmonitor_worker = None
        self.erv_worker = None
        self.cvonline_worker = None
        self.humancentrum_worker = None
        self.kozigallas_worker = None
        self.pannonwork_worker = None
        self.borsodchem_worker = None
        self.threads = []

        self.input_data = input_data
        self.portals = input_data["portals"]

        self.parent = parent
        self.tabwidget = self.parent.parent.tabwidget
        self.jobs_tab = self.parent.parent.jobs_tab
        self.jobs_tab.output_panel.itemDoubleClicked.connect(self.open_url)

        self.progressbar = self.jobs_tab.progressbar
        self.cancel_btn = self.jobs_tab.abort_btn

        self.portal_switch()

    def prepare_output_panel(self):
        self.jobs_tab.output_panel.clear()
        self.tabwidget.setCurrentIndex(1)
        self.show_progressbar_and_btn()

    def show_progressbar_and_btn(self):
        self.progressbar.setVisible(True)
        self.cancel_btn.setVisible(True)

    def hide_progressbar_and_btn(self):
        self.progressbar.setVisible(False)
        self.cancel_btn.setVisible(False)

    def error_msg(self, portal_name, message, page_url):
        self.jobs_tab.output_panel.addItem(ErrorMessageItem(portal_name, message, page_url))
        self.jobs_tab.output_panel.scrollToBottom()
        self.error_counter += 1

    def found_job(self, found_job_dict):
        portal_name = found_job_dict["portal_name"]
        job = found_job_dict["job"]
        job_link = found_job_dict["job_link"]

        self.jobs_tab.output_panel.addItem(JobItem(portal_name, job, job_link))
        self.jobs_tab.output_panel.scrollToBottom()
        self.found_job_counter += 1

    def jobs_search_finished(self):
        self.number_of_active_portals -= 1
        if not self.number_of_active_portals:
            if self.found_job_counter and not self.error_counter:
                self.hide_progressbar_and_btn()
                PopupWindow(self.parent, f"A keresési feltételek alapján {self.found_job_counter} db állást találtam!", "information")
                self.parent.keywords_input.setFocus()
            elif self.found_job_counter and self.error_counter:
                self.hide_progressbar_and_btn()
                PopupWindow(self.parent, f"A keresési feltételek alapján {self.found_job_counter} db állást találtam!\n"
                                         f"Azonban hibák fordultak elő!\n"
                                         f"Lásd: piros sorok!", "warning")
                self.parent.keywords_input.setFocus()
            elif not self.found_job_counter and not self.error_counter:
                self.hide_progressbar_and_btn()
                PopupWindow(self.parent, "Nincs megfelelő állásajánlat!", "information")
                self.tabwidget.setCurrentIndex(0)
                self.parent.keywords_input.setFocus()
            else:
                self.hide_progressbar_and_btn()
                PopupWindow(self.parent, "Nincs megfelelő állásajánlat!\n"
                                         f"Azonban hibák fordultak elő!\n"
                                         f"Lásd: piros sorok!", "warning")
                self.parent.keywords_input.setFocus()

    def open_url(self, other):
        url = other.url
        QDesktopServices.openUrl(QUrl(url))

    def portal_switch(self):
        if not self.number_of_active_portals and self.portals:
            self.prepare_output_panel()
        if "Profession (profession.hu)" in self.portals:
            self.profession_start()
            self.threads.append(self.profession_worker)
            self.number_of_active_portals += 1
        if "Evosoft (evosoft.hu)" in self.portals:
            self.evosoft_start()
            self.threads.append(self.evosoft_worker)
            self.number_of_active_portals += 1
        if "Bosch (bosch.hu)" in self.portals:
            self.bosch_start()
            self.threads.append(self.bosch_worker)
            self.number_of_active_portals += 1
        if "Állás.Club (allas.club)" in self.portals:
            self.allas_club_start()
            self.threads.append(self.allas_club_worker)
            self.number_of_active_portals += 1
        if "Virtuális Munkaerőpiac Portál (vmp.munka.hu)" in self.portals:
            self.vmp_start()
            self.threads.append(self.vmp_worker)
            self.number_of_active_portals += 1
        if "Jobmonitor (jobmonitor.hu)" in self.portals:
            self.jobmonitor_start()
            self.threads.append(self.jobmonitor_worker)
            self.number_of_active_portals += 1
        if "ÉRV (ervzrt.hu)" in self.portals:
            self.erv_start()
            self.threads.append(self.erv_worker)
            self.number_of_active_portals += 1
        if "Cvonline (cvonline.hu)" in self.portals:
            self.cvonline_start()
            self.threads.append(self.cvonline_worker)
            self.number_of_active_portals += 1
        if "Humán Centrum (humancentrum.hu)" in self.portals:
            self.humancentrum_start()
            self.threads.append(self.humancentrum_worker)
            self.number_of_active_portals += 1
        if "Közigállás (kozigallas.gov.hu)" in self.portals:
            self.kozigallas_start()
            self.threads.append(self.kozigallas_worker)
            self.number_of_active_portals += 1
        if "Pannonwork (allas.pannonwork.hu)" in self.portals:
            self.pannonwork_start()
            self.threads.append(self.pannonwork_worker)
            self.number_of_active_portals += 1
        if "Borsodchem (karrier.borsodchem.eu)" in self.portals:
            self.borsodchem_start()
            self.threads.append(self.borsodchem_worker)
            self.number_of_active_portals += 1

    def profession_start(self):
        self.profession_worker = ProfessionWorker(self.input_data)
        self.profession_worker.setTerminationEnabled(True)
        self.profession_worker.found_job.connect(self.found_job)
        self.profession_worker.search_finished.connect(self.jobs_search_finished)
        self.profession_worker.error_msg.connect(self.error_msg)
        self.profession_worker.start()

    def evosoft_start(self):
        self.evosoft_worker = EvosoftWorker(self.input_data)
        self.evosoft_worker.setTerminationEnabled(True)
        self.evosoft_worker.found_job.connect(self.found_job)
        self.evosoft_worker.search_finished.connect(self.jobs_search_finished)
        self.evosoft_worker.error_msg.connect(self.error_msg)
        self.evosoft_worker.start()

    def bosch_start(self):
        self.bosch_worker = BoschWorker(self.input_data)
        self.bosch_worker.setTerminationEnabled(True)
        self.bosch_worker.found_job.connect(self.found_job)
        self.bosch_worker.search_finished.connect(self.jobs_search_finished)
        self.bosch_worker.error_msg.connect(self.error_msg)
        self.bosch_worker.start()

    def allas_club_start(self):
        self.allas_club_worker = AllasClubWorker(self.input_data)
        self.allas_club_worker.setTerminationEnabled(True)
        self.allas_club_worker.found_job.connect(self.found_job)
        self.allas_club_worker.search_finished.connect(self.jobs_search_finished)
        self.allas_club_worker.error_msg.connect(self.error_msg)
        self.allas_club_worker.start()

    def vmp_start(self):
        self.vmp_worker = VMPWorker(self.input_data)
        self.vmp_worker.setTerminationEnabled(True)
        self.vmp_worker.error_msg.connect(self.error_msg)
        self.vmp_worker.found_job.connect(self.found_job)
        self.vmp_worker.search_finished.connect(self.jobs_search_finished)
        self.vmp_worker.start()

    def jobmonitor_start(self):
        self.jobmonitor_worker = JobmonitorWorker(self.input_data)
        self.jobmonitor_worker.setTerminationEnabled(True)
        self.jobmonitor_worker.error_msg.connect(self.error_msg)
        self.jobmonitor_worker.found_job.connect(self.found_job)
        self.jobmonitor_worker.search_finished.connect(self.jobs_search_finished)
        self.jobmonitor_worker.start()

    def erv_start(self):
        self.erv_worker = ERVWorker(self.input_data)
        self.erv_worker.setTerminationEnabled(True)
        self.erv_worker.error_msg.connect(self.error_msg)
        self.erv_worker.found_job.connect(self.found_job)
        self.erv_worker.search_finished.connect(self.jobs_search_finished)
        self.erv_worker.start()

    def cvonline_start(self):
        self.cvonline_worker = CvonlineWorker(self.input_data)
        self.cvonline_worker.setTerminationEnabled(True)
        self.cvonline_worker.error_msg.connect(self.error_msg)
        self.cvonline_worker.found_job.connect(self.found_job)
        self.cvonline_worker.search_finished.connect(self.jobs_search_finished)
        self.cvonline_worker.start()

    def humancentrum_start(self):
        self.humancentrum_worker = HumancentrumWorker(self.input_data)
        self.humancentrum_worker.setTerminationEnabled(True)
        self.humancentrum_worker.error_msg.connect(self.error_msg)
        self.humancentrum_worker.found_job.connect(self.found_job)
        self.humancentrum_worker.search_finished.connect(self.jobs_search_finished)
        self.humancentrum_worker.start()

    def kozigallas_start(self):
        self.kozigallas_worker = KozigallasWorker(self.input_data)
        self.kozigallas_worker.setTerminationEnabled(True)
        self.kozigallas_worker.error_msg.connect(self.error_msg)
        self.kozigallas_worker.found_job.connect(self.found_job)
        self.kozigallas_worker.search_finished.connect(self.jobs_search_finished)
        self.kozigallas_worker.start()

    def pannonwork_start(self):
        self.pannonwork_worker = PannonworkWorker(self.input_data)
        self.pannonwork_worker.setTerminationEnabled(True)
        self.pannonwork_worker.error_msg.connect(self.error_msg)
        self.pannonwork_worker.found_job.connect(self.found_job)
        self.pannonwork_worker.search_finished.connect(self.jobs_search_finished)
        self.pannonwork_worker.start()

    def borsodchem_start(self):
        self.borsodchem_worker = BorsodchemWorker(self.input_data)
        self.borsodchem_worker.setTerminationEnabled(True)
        self.borsodchem_worker.error_msg.connect(self.error_msg)
        self.borsodchem_worker.found_job.connect(self.found_job)
        self.borsodchem_worker.search_finished.connect(self.jobs_search_finished)
        self.borsodchem_worker.start()


class JobItem(QListWidgetItem):
    def __init__(self, portal_name, job, job_link):
        super().__init__()
        self.portal_name = portal_name
        self.job = job
        self.url = job_link
        self.setText(f"[{portal_name}] {job}")


class ErrorMessageItem(QListWidgetItem):
    def __init__(self, portal_name, message, url):
        super().__init__()
        self.portal_name = portal_name
        self.message = message
        self.url = url
        self.setText(f"[{portal_name}] {message}")
        self.setTextColor(QColor("red"))
