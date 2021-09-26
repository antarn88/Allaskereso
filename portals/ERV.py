from socket import error

from PySide2.QtCore import QThread, Signal
from bs4 import BeautifulSoup
from requests import get


class ERVWorker(QThread):
    job = Signal(dict)
    found_job = Signal(dict)
    search_finished = Signal()
    error_msg = Signal(str, str, str)

    def __init__(self, input_data):
        super(ERVWorker, self).__init__()

        # App attributes
        self.PORTAL_NAME = "ÉRV"
        self.PORTAL_URL = "https://www.ervzrt.hu"
        self.variable_page_url = None

        # Get data from user input data
        self.jobs = input_data["jobs"]
        self.exclude_words = input_data["exclude_words"]
        self.search_location = input_data["search_location"]

        self.variable_page_url_changer()

    def run(self):
        try:
            self.get_jobs()
        except AttributeError:
            # For debugging
            # from traceback import print_exc
            # print_exc()

            self.error_msg.emit(self.PORTAL_NAME,
                                "A portál forráskódjában fontos változások történtek, a program frissítésre szorul!",
                                self.PORTAL_URL)
        except error:
            self.error_msg.emit(self.PORTAL_NAME,
                                "Hálózati hiba történt!",
                                self.PORTAL_URL)

        self.search_finished.emit()

    def variable_page_url_changer(self):
        for location in get_location_url_dict():
            if location == self.search_location:
                self.variable_page_url = get_location_url_dict()[location]

    def get_jobs(self):
        soup = get_soup(self.variable_page_url)
        if soup:
            jobs = soup.select("#main-container .careers article")
            for job in jobs:
                job_name = job.select_one(".no-margin a").text.strip().title()
                job_link = str(job.select_one(".no-margin a").get("href")).strip()
                self.job.emit(get_data_dict(self.PORTAL_NAME, job_name, job_link))
                for searched_job in self.jobs:
                    job_ok = True
                    if self.exclude_words != ['']:
                        for exclude_word in self.exclude_words:
                            if exclude_word.lower() in job_name.lower():
                                job_ok = False
                                break
                        if searched_job in job_name.lower() and job_ok:
                            self.found_job.emit(get_data_dict(self.PORTAL_NAME, job_name, job_link))
                    else:
                        if searched_job in job_name.lower():
                            self.found_job.emit(get_data_dict(self.PORTAL_NAME, job_name, job_link))


def get_soup(url):
    if url:
        headers = {"user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"
                                 " (KHTML, like Gecko) Chrome/89.0.4389.82 Safari/537.36"}
        return BeautifulSoup(get(url, headers=headers).text, "lxml")


def get_data_dict(portal_name, job, job_link):
    return {
        "portal_name": portal_name,
        "job": job,
        "job_link": job_link
    }


def get_location_url_dict():
    return {
        "Borsod-Abaúj-Zemplén megye":
            "https://www.ervzrt.hu/karrier"
    }
