from socket import error

from PySide2.QtCore import QThread, Signal
from bs4 import BeautifulSoup
from requests import get


class HumancentrumWorker(QThread):
    job = Signal(dict)
    found_job = Signal(dict)
    search_finished = Signal()
    error_msg = Signal(str, str, str)

    def __init__(self, input_data):
        super(HumancentrumWorker, self).__init__()

        # App attributes
        self.PORTAL_NAME = "Humán Centrum"
        self.PORTAL_URL = "https://www.humancentrum.hu/"
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
            if soup:
                has_next_page = bool(soup.select_one(".next-page"))
                job_cards = soup.select(".cs-post-title")
                for job_card in job_cards:
                    job_name = job_card.select_one("h5 a").getText()
                    job_link = f"{self.PORTAL_URL}{job_card.select_one('h5 a').get('href')}"
                    self.job.emit(get_data_dict(self.PORTAL_NAME, job_name, job_link))
                    for searched_job in self.jobs:
                        if searched_job in job_name.lower():
                            self.found_job.emit(get_data_dict(self.PORTAL_NAME, job_name, job_link))
                self.page_counter += 1
            else:
                break


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


def get_location_url_dict(page_counter):
    return {
        "Bács-Kiskun megye":
            f"https://www.humancentrum.hu/allasok?search=&office%5B%5D=5&page={page_counter}",
        "Baranya megye":
            f"https://www.humancentrum.hu/allasok?search=&office%5B%5D=11&page={page_counter}",
        "Békés megye":
            f"https://www.humancentrum.hu/allasok?search=&office%5B%5D=14&page={page_counter}",
        "Borsod-Abaúj-Zemplén megye":
            f"https://www.humancentrum.hu/allasok?search=&office%5B%5D=6&page={page_counter}",
        "Budapest":
            f"https://www.humancentrum.hu/allasok?search=&office%5B%5D=1&page={page_counter}",
        "Csongrád-Csanád megye":
            f"https://www.humancentrum.hu/allasok?search=&office%5B%5D=3&page={page_counter}",
        "Fejér megye":
            f"https://www.humancentrum.hu/allasok?search=&office%5B%5D=9&page={page_counter}",
        "Győr-Moson-Sopron megye":
            f"https://www.humancentrum.hu/allasok?search=&office%5B%5D=10&page={page_counter}",
        "Hajdú-Bihar megye":
            f"https://www.humancentrum.hu/allasok?search=&office%5B%5D=2&page={page_counter}",
        "Heves megye":
            f"https://www.humancentrum.hu/allasok?search=&office%5B%5D=17&office%5B%5D=20&page={page_counter}",
        "Jász-Nagykun-Szolnok megye":
            f"https://www.humancentrum.hu/allasok?search=&office%5B%5D=4&page={page_counter}",
        "Komárom-Esztergom megye":
            f"https://www.humancentrum.hu/allasok?search=&office%5B%5D=22&page={page_counter}",
        "Pest megye":
            f"https://www.humancentrum.hu/allasok?search=&office%5B%5D=18&page={page_counter}",
        "Somogy megye":
            f"https://www.humancentrum.hu/allasok?search=&office%5B%5D=13&page={page_counter}",
        "Szabolcs-Szatmár-Bereg megye":
            f"https://www.humancentrum.hu/allasok?search=&office%5B%5D=15&page={page_counter}",
        "Vas megye":
            f"https://www.humancentrum.hu/allasok?search=&office%5B%5D=12&page={page_counter}",
        "Veszprém megye":
            f"https://www.humancentrum.hu/allasok?search=&office%5B%5D=7&page={page_counter}",
        "Zala megye":
            f"https://www.humancentrum.hu/allasok?search=&office%5B%5D=21&office%5B%5D=8&page={page_counter}"
    }
