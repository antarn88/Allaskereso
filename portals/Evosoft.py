from socket import error

from PySide2.QtCore import QThread, Signal
from bs4 import BeautifulSoup
from requests import get


class EvosoftWorker(QThread):
    job = Signal(dict)
    found_job = Signal(dict)
    search_finished = Signal()
    error_msg = Signal(str, str, str)

    def __init__(self, input_data):
        super(EvosoftWorker, self).__init__()

        # App attributes
        self.PORTAL_NAME = "Evosoft"
        self.PORTAL_URL = "https://karrier.evosoft.hu"
        self.url = None

        # Get data from user input data
        self.jobs = input_data["jobs"]
        self.search_location = input_data["search_location"]

        self.search_location_url_switch()

    def run(self):
        try:
            if self.url:
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

    def search_location_url_switch(self):
        for location in get_location_url_dict():
            if location == self.search_location:
                self.url = get_location_url_dict()[location]

    def get_jobs(self):
        for i in get_soup(self.url).html.body.find_all("h3"):
            job = str(i.a.text).strip()
            job_link = f"https://karrier.evosoft.hu{i.a['href']}".strip()
            self.job.emit(get_data_dict(self.PORTAL_NAME, job, job_link))
            for searched_job in self.jobs:
                if searched_job in job.lower():
                    self.found_job.emit(get_data_dict(self.PORTAL_NAME, job, job_link))


def get_soup(url):
    headers = {"user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"
                             " (KHTML, like Gecko) Chrome/89.0.4389.82 Safari/537.36"}
    html_text = get(url, headers=headers).text
    return BeautifulSoup(html_text, "lxml")


def get_data_dict(portal_name, job, job_link):
    return {
        "portal_name": portal_name,
        "job": job,
        "job_link": job_link
    }


def get_location_url_dict():
    return {
        "Borsod-Abaúj-Zemplén megye":
            f"https://karrier.evosoft.hu/?filter%5Btechnology%5D=ALL&filter%5Blocation%5D=3",
        "Budapest":
            f"https://karrier.evosoft.hu/?filter%5Btechnology%5D=ALL&filter%5Blocation%5D=1",
        "Csongrád-Csanád megye":
            f"https://karrier.evosoft.hu/?filter%5Btechnology%5D=ALL&filter%5Blocation%5D=2"
    }
