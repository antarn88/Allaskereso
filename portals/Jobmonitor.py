from socket import error

from PySide2.QtCore import QThread, Signal
from bs4 import BeautifulSoup
from requests import get


class JobmonitorWorker(QThread):
    job = Signal(dict)
    found_job = Signal(dict)
    search_finished = Signal()
    error_msg = Signal(str, str, str)

    def __init__(self, input_data):
        super(JobmonitorWorker, self).__init__()

        # App attributes
        self.PORTAL_NAME = "Jobmonitor"
        self.PORTAL_URL = "https://www.jobmonitor.hu"
        self.variable_page_url = None
        self.page_counter = 1

        # Get data from user input data
        self.jobs = input_data["jobs"]
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
        for location in get_location_url_dict(self.page_counter):
            if location == self.search_location:
                self.variable_page_url = get_location_url_dict(self.page_counter)[location]

    def get_jobs(self):
        has_next_page = True
        while has_next_page:
            self.variable_page_url_changer()
            soup = get_soup(self.variable_page_url)
            has_next_page = bool(soup.select_one("#content .column_middle .pagingbox #next"))
            job_cards = soup.select("#content .column_middle .listbox ul .lister-item")
            for job_card in job_cards:
                job_name = str(job_card.select_one(".allasNeve").text).strip().replace("  ", " ")
                job_link = f"{self.PORTAL_URL}{job_card.select_one('.allasNeve').get('href')}".strip()
                self.job.emit(get_data_dict(self.PORTAL_NAME, job_name, job_link))
                for searched_job in self.jobs:
                    if searched_job in job_name.lower():
                        self.found_job.emit(get_data_dict(self.PORTAL_NAME, job_name, job_link))
            self.page_counter += 1


def get_soup(url):
    headers = {"user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"
                             " (KHTML, like Gecko) Chrome/89.0.4389.82 Safari/537.36"}
    return BeautifulSoup(get(url, headers=headers).text, "lxml")


def get_data_dict(portal_name, job, job_link):
    return {
        "portal_name": portal_name,
        "job": job,
        "job_link": job_link
    }


def get_location_url_dict(page_counter):
    return {
        "Bács-Kiskun megye":
            f"https://www.jobmonitor.hu/allasok/bacs-kiskun/_104%2C{page_counter}",
        "Baranya megye":
            f"https://www.jobmonitor.hu/allasok/baranya/_101%2C{page_counter}",
        "Békés megye":
            f"https://www.jobmonitor.hu/allasok/bekes/_105%2C{page_counter}",
        "Borsod-Abaúj-Zemplén megye":
            f"https://www.jobmonitor.hu/allasok/borsod-abauj-zemplen/_102%2C{page_counter}",
        "Budapest":
            f"https://www.jobmonitor.hu/allasok/budapest/_103%2C{page_counter}",
        "Csongrád-Csanád megye":
            f"https://www.jobmonitor.hu/allasok/csongrad/_106%2C{page_counter}",
        "Fejér megye":
            f"https://www.jobmonitor.hu/allasok/fejer/_107%2C{page_counter}",
        "Győr-Moson-Sopron megye":
            f"https://www.jobmonitor.hu/allasok/gyor-moson-sopron/_108%2C{page_counter}",
        "Hajdú-Bihar megye":
            f"https://www.jobmonitor.hu/allasok/hajdu-bihar/_109%2C{page_counter}",
        "Heves megye":
            f"https://www.jobmonitor.hu/allasok/heves/_110%2C{page_counter}",
        "Jász-Nagykun-Szolnok megye":
            f"https://www.jobmonitor.hu/allasok/jasz-nagykun-szolnok/_111%2C{page_counter}",
        "Komárom-Esztergom megye":
            f"https://www.jobmonitor.hu/allasok/komarom-esztergom/_112%2C{page_counter}",
        "Nógrád megye":
            f"https://www.jobmonitor.hu/allasok/nograd/_113%2C{page_counter}",
        "Pest megye":
            f"https://www.jobmonitor.hu/allasok/pest/_114%2C{page_counter}",
        "Somogy megye":
            f"https://www.jobmonitor.hu/allasok/somogy/_115%2C{page_counter}",
        "Szabolcs-Szatmár-Bereg megye":
            f"https://www.jobmonitor.hu/allasok/szabolcs-szatmar-bereg/_116%2C{page_counter}",
        "Tolna megye":
            f"https://www.jobmonitor.hu/allasok/tolna/_117%2C{page_counter}",
        "Vas megye":
            f"https://www.jobmonitor.hu/allasok/vas/_118%2C{page_counter}",
        "Veszprém megye":
            f"https://www.jobmonitor.hu/allasok/veszprem/_119%2C{page_counter}",
        "Zala megye":
            f"https://www.jobmonitor.hu/allasok/zala/_120%2C{page_counter}"
    }
