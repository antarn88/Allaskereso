from socket import error

from PySide2.QtCore import QThread, Signal
from bs4 import BeautifulSoup
from requests import get


class AllasClubWorker(QThread):
    job = Signal(dict)
    found_job = Signal(dict)
    search_finished = Signal()
    error_msg = Signal(str, str, str)

    def __init__(self, input_data):
        super(AllasClubWorker, self).__init__()

        # App attributes
        self.PORTAL_NAME = "Állás.Club"
        self.PORTAL_URL = "https://allas.club"
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
        while True:
            self.variable_page_url_changer()
            soup = get_soup(self.variable_page_url)
            current = int(soup.html.body.select("span.current")[-1].text)
            last = int(soup.html.body.select("a.page")[-1].text)
            for a_tag in soup.html.body.find_all("a", id="linkem"):
                job = str(a_tag.text).strip()
                job_link = str(a_tag["href"]).strip()
                self.job.emit(get_data_dict(self.PORTAL_NAME, job, job_link))
                for searched_job in self.jobs:
                    if searched_job in job.lower() and job:
                        self.found_job.emit(get_data_dict(self.PORTAL_NAME, job, job_link))
            if current == last + 1:
                break
            self.page_counter += 1


def get_soup(url):
    headers = {"user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/89.0.4389.82 Safari/537.36"}
    html_text = get(url, headers=headers).text
    return BeautifulSoup(html_text, "lxml")


def get_data_dict(portal_name, job, job_link):
    return {
        "portal_name": portal_name,
        "job": job,
        "job_link": job_link
    }


def get_location_url_dict(page_counter):
    return {
        "Bács-Kiskun megye":
            f"https://allas.club/search/%20/page/{page_counter}/?megye=B%C3%A1cs-Kiskun%2CMagyarorsz%C3%A1g",
        "Baranya megye":
            f"https://allas.club/search/%20/page/{page_counter}/?megye=Baranya%2CMagyarorsz%C3%A1g",
        "Békés megye":
            f"https://allas.club/search/%20/page/{page_counter}/?megye=B%C3%A9k%C3%A9s%2CMagyarorsz%C3%A1g",
        "Borsod-Abaúj-Zemplén megye":
            f"https://allas.club/search/%20/page/{page_counter}/?megye=Borsod-Aba%C3%BAj-Zempl%C3%A9n,Magyarorsz%C3%A1g",
        "Budapest":
            f"https://allas.club/search/%20/page/{page_counter}/?hol=Budapest",
        "Csongrád-Csanád megye":
            f"https://allas.club/search/%20/page/{page_counter}/?megye=Csongr%C3%A1d%2CMagyarorsz%C3%A1g",
        "Fejér megye":
            f"https://allas.club/search/%20/page/{page_counter}/?megye=Fej%C3%A9r,Magyarorsz%C3%A1g",
        "Győr-Moson-Sopron megye":
            f"https://allas.club/search/%20/page/{page_counter}/?megye=Gy%C5%91r-Moson-Sopron,Magyarorsz%C3%A1g",
        "Hajdú-Bihar megye":
            f"https://allas.club/search/%20/page/{page_counter}/?megye=Hajd%C3%BA-Bihar,Magyarorsz%C3%A1g",
        "Heves megye":
            f"https://allas.club/search/%20/page/{page_counter}/?megye=Heves,Magyarorsz%C3%A1g",
        "Jász-Nagykun-Szolnok megye":
            f"https://allas.club/search/%20/page/{page_counter}/?megye=J%C3%A1sz-Nagykun-Szolnok,Magyarorsz%C3%A1g",
        "Komárom-Esztergom megye":
            f"https://allas.club/search/%20/page/{page_counter}/?megye=Kom%C3%A1rom-Esztergom,Magyarorsz%C3%A1g",
        "Nógrád megye":
            f"https://allas.club/search/%20/page/{page_counter}/?megye=N%C3%B3gr%C3%A1d,Magyarorsz%C3%A1g",
        "Pest megye":
            f"https://allas.club/search/%20/page/{page_counter}/?megye=Pest,Magyarorsz%C3%A1g",
        "Somogy megye":
            f"https://allas.club/search/%20/page/{page_counter}/?megye=Somogy,Magyarorsz%C3%A1g",
        "Szabolcs-Szatmár-Bereg megye":
            f"https://allas.club/search/%20/page/{page_counter}/?megye=Szabolcs-Szatm%C3%A1r-Bereg,Magyarorsz%C3%A1g",
        "Tolna megye":
            f"https://allas.club/search/%20/page/{page_counter}/?megye=Tolna,Magyarorsz%C3%A1g",
        "Vas megye":
            f"https://allas.club/search/%20/page/{page_counter}/?megye=Vas,Magyarorsz%C3%A1g",
        "Veszprém megye":
            f"https://allas.club/search/%20/page/{page_counter}/?megye=Veszpr%C3%A9m,Magyarorsz%C3%A1g",
        "Zala megye":
            f"https://allas.club/search/%20/page/{page_counter}/?megye=Zala,Magyarorsz%C3%A1g"
    }
