from socket import error

from PySide2.QtCore import QThread, Signal
from bs4 import BeautifulSoup
from requests import get


class ProfessionWorker(QThread):
    job = Signal(dict)
    found_job = Signal(dict)
    search_finished = Signal()
    error_msg = Signal(str, str, str)

    def __init__(self, input_data):
        super(ProfessionWorker, self).__init__()

        # App attributes
        self.PORTAL_NAME = "Profession"
        self.PORTAL_URL = "https://www.profession.hu"
        self.first_page_url = None
        self.variable_page_url = None
        self.page_counter = 1

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
        for location in get_location_url_dict(self.page_counter):
            if location == self.search_location:
                self.variable_page_url = get_location_url_dict(self.page_counter)[location]

    def get_jobs(self):
        self.page_counter = get_active_page(self.variable_page_url)
        while not self.page_counter == get_last_page(self.variable_page_url) + 1:
            self.variable_page_url_changer()
            for i in get_soup(self.variable_page_url).html.body.find_all("div", class_="card-body"):
                job = str(i.a.text).strip()
                job_link = str(i.h2.a["href"]).strip()
                self.job.emit(get_data_dict(self.PORTAL_NAME, job, job_link))
                for searched_job in self.jobs:
                    job_ok = True
                    if self.exclude_words != ['']:
                        for exclude_word in self.exclude_words:
                            if exclude_word.lower() in job.lower():
                                job_ok = False
                                break
                        if searched_job in job.lower() and job_ok:
                            self.found_job.emit(get_data_dict(self.PORTAL_NAME, job, job_link))
                    else:
                        if searched_job in job.lower():
                            self.found_job.emit(get_data_dict(self.PORTAL_NAME, job, job_link))
            self.page_counter += 1


def get_soup(url):
    headers = {"user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/89.0.4389.82 Safari/537.36"}
    return BeautifulSoup(get(url, headers=headers).text, "lxml")


def get_active_page(portal_url):
    return int(get_soup(portal_url).html.body.find("span", class_="active").text)


def get_last_page(portal_url):
    try:
        return int(get_soup(portal_url).html.body.find("span", class_="jump-forward").a["data-total"])
    except AttributeError:
        return int(get_soup(portal_url).html.body.find("span", class_="jump-backward").a["data-total"])


def get_data_dict(portal_name, job, job_link):
    return {
        "portal_name": portal_name,
        "job": job,
        "job_link": job_link
    }


def get_location_url_dict(page_counter):
    return {
        "Bács-Kiskun megye":
            f"https://www.profession.hu/allasok/bacs-kiskun/{page_counter},0,25,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,15",
        "Baranya megye":
            f"https://www.profession.hu/allasok/baranya/{page_counter},0,26,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,15",
        "Békés megye":
            f"https://www.profession.hu/allasok/bekes/{page_counter},0,27,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,15",
        "Borsod-Abaúj-Zemplén megye":
            f"https://www.profession.hu/allasok/borsod-abauj-zemplen/{page_counter},0,28,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,15",
        "Budapest":
            f"https://www.profession.hu/allasok/budapest/{page_counter},0,23,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,15",
        "Csongrád-Csanád megye":
            f"https://www.profession.hu/allasok/csongrad/{page_counter},0,29,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,15",
        "Fejér megye":
            f"https://www.profession.hu/allasok/fejer/{page_counter},0,30,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,15",
        "Győr-Moson-Sopron megye":
            f"https://www.profession.hu/allasok/gyor-moson-sopron/{page_counter},0,31,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,15",
        "Hajdú-Bihar megye":
            f"https://www.profession.hu/allasok/hajdu-bihar/{page_counter},0,32,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,15",
        "Heves megye":
            f"https://www.profession.hu/allasok/heves/{page_counter},0,33,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,15",
        "Jász-Nagykun-Szolnok megye":
            f"https://www.profession.hu/allasok/jasz-nagykun-szolnok/{page_counter},0,34,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,15",
        "Komárom-Esztergom megye":
            f"https://www.profession.hu/allasok/komarom-esztergom/{page_counter},0,35,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,15",
        "Nógrád megye":
            f"https://www.profession.hu/allasok/nograd/{page_counter},0,36,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,15",
        "Pest megye":
            f"https://www.profession.hu/allasok/pest/{page_counter},0,37,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,15",
        "Somogy megye":
            f"https://www.profession.hu/allasok/somogy/{page_counter},0,38,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,15",
        "Szabolcs-Szatmár-Bereg megye":
            f"https://www.profession.hu/allasok/szabolcs-szatmar-bereg/{page_counter},0,39,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,15",
        "Tolna megye":
            f"https://www.profession.hu/allasok/tolna/{page_counter},0,40,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,15",
        "Vas megye":
            f"https://www.profession.hu/allasok/vas/{page_counter},0,41,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,15",
        "Veszprém megye":
            f"https://www.profession.hu/allasok/veszprem/{page_counter},0,42,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,15",
        "Zala megye":
            f"https://www.profession.hu/allasok/zala/{page_counter},0,43,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,15"
    }
