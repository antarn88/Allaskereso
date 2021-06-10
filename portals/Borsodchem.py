from socket import error
from time import sleep

from PySide2.QtCore import QThread, Signal
from bs4 import BeautifulSoup
from chromedriver_autoinstaller import install
from selenium import webdriver
from selenium.common.exceptions import StaleElementReferenceException, NoSuchElementException
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions
from selenium.webdriver.support.wait import WebDriverWait


class BorsodchemWorker(QThread):
    job = Signal(dict)
    found_job = Signal(dict)
    search_finished = Signal()
    error_msg = Signal(str, str, str)

    def __init__(self, input_data):
        super(BorsodchemWorker, self).__init__()

        # App attributes
        self.PORTAL_NAME = "Borsodchem"
        self.PORTAL_URL = "https://career2.successfactors.eu/career?company=borsodchem"
        self.driver = None

        # Get data from user input data
        self.jobs = input_data["jobs"]
        self.search_location = input_data["search_location"]

    def run(self):
        try:
            if self.search_location == "Borsod-Abaúj-Zemplén megye":
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

    def prepare_selenium(self):
        install()
        chrome_options = webdriver.ChromeOptions()
        chrome_options.headless = True
        self.driver = webdriver.Chrome(options=chrome_options)

    def navigate_to_jobs(self):
        self.driver.get(self.PORTAL_URL)
        wait = WebDriverWait(self.driver, 10)
        wait.until(expected_conditions.element_to_be_clickable((By.CLASS_NAME, 'left_panel')))
        search_button = wait.until(expected_conditions.element_to_be_clickable((By.CSS_SELECTOR, ".globalRoundedCornersXSmall.globalPrimaryButton")))
        search_button.click()
        wait.until(expected_conditions.visibility_of_element_located((By.CSS_SELECTOR, ".jobTitle")))

    def get_jobs(self):
        while True:
            jobs = self.driver.find_elements_by_css_selector(".jobTitle")
            for job in jobs:
                soup = BeautifulSoup(job.get_attribute('outerHTML'), "lxml")
                job_name = str(soup.select_one("a").text).strip()
                job_link = f'https://career2.successfactors.eu{str(soup.select_one("a").get("href")).strip()}'
                self.job.emit(get_data_dict(self.PORTAL_NAME, job_name, job_link))
                for searched_job in self.jobs:
                    if searched_job in job_name.lower():
                        self.found_job.emit(get_data_dict(self.PORTAL_NAME, job_name, job_link))
            try:
                self.driver.find_element_by_xpath('//a[@title="Következő oldal"]').click()
                sleep(3)
            except (StaleElementReferenceException, NoSuchElementException):
                self.driver.quit()
                break


def get_data_dict(portal_name, job, job_link):
    return {
        "portal_name": portal_name,
        "job": job,
        "job_link": job_link
    }
