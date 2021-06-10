from socket import error

from PySide2.QtCore import QThread, Signal
from chromedriver_autoinstaller import install
from selenium import webdriver
from selenium.webdriver.support.select import Select


class KozigallasWorker(QThread):
    job = Signal(dict)
    found_job = Signal(dict)
    search_finished = Signal()
    error_msg = Signal(str, str, str)

    def __init__(self, input_data):
        super(KozigallasWorker, self).__init__()

        # App attributes
        self.PORTAL_NAME = "Közigállás"
        self.PORTAL_URL = "https://kozigallas.gov.hu/publicsearch.aspx"
        self.driver = None

        # Get data from user input data
        self.jobs = input_data["jobs"]
        self.search_location = input_data["search_location"]

    def run(self):
        try:
            self.correct_location()
            self.prepare_selenium()
            self.navigate_to_jobs()
            self.get_jobs()
        except AttributeError:
            self.error_msg.emit(self.PORTAL_NAME,
                                "A portál forráskódjában fontos változások történtek, a program frissítésre szorul!",
                                self.PORTAL_URL)
        except error:
            self.error_msg.emit(self.PORTAL_NAME,
                                "Hálózati hiba történt!",
                                self.PORTAL_URL)

        self.search_finished.emit()

    def correct_location(self):
        self.search_location = "Csongrád megye" if self.search_location == "Csongrád-Csanád megye" else self.search_location

    def prepare_selenium(self):
        install()
        chrome_options = webdriver.ChromeOptions()
        chrome_options.headless = True
        self.driver = webdriver.Chrome(options=chrome_options)

    def navigate_to_jobs(self):
        self.driver.get(self.PORTAL_URL)
        switch_to_detailed_search_link = self.driver.find_element_by_css_selector("#ctl00_ContentPlaceHolder1_JobSearchForm1_lnkDetailedSearch")
        switch_to_detailed_search_link.click()
        county_select = Select(self.driver.find_element_by_css_selector("#ctl00_ContentPlaceHolder1_JobSearchForm1_ddlCounty"))
        county_select.select_by_visible_text(self.search_location)
        search_button = self.driver.find_element_by_css_selector("#ctl00_ContentPlaceHolder1_JobSearchForm1_btnSearch")
        search_button.click()

    def get_jobs(self):
        has_next_page = True
        while has_next_page:
            has_next_page = self.driver.find_elements_by_css_selector("#ctl00_ContentPlaceHolder1_JobSearchForm1_JobList1_linkNext2")
            jobs = self.driver.find_elements_by_css_selector(".jobapplication")
            for job in jobs:
                job_name = str(job.text).strip()
                job_id = str(job.get_attribute("href")).split("'")[1].strip()
                job_link = f"https://kozigallas.gov.hu/pages/jobviewer.aspx?ID={job_id}"
                self.job.emit(get_data_dict(self.PORTAL_NAME, job_name, job_link))
                for searched_job in self.jobs:
                    if searched_job in job_name.lower():
                        self.found_job.emit(get_data_dict(self.PORTAL_NAME, job_name, job_link))
            if has_next_page:
                has_next_page[0].click()
        self.driver.quit()


def get_data_dict(portal_name, job, job_link):
    return {
        "portal_name": portal_name,
        "job": job,
        "job_link": job_link
    }
