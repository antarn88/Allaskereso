from socket import error

from PySide2.QtCore import QThread, Signal
from bs4 import BeautifulSoup
from requests import get


class BoschWorker(QThread):
    job = Signal(dict)
    found_job = Signal(dict)
    search_finished = Signal()
    error_msg = Signal(str, str, str)

    def __init__(self, input_data):
        super(BoschWorker, self).__init__()

        # App attributes
        self.PORTAL_NAME = "Bosch"
        self.PORTAL_URL = "https://careers.smartrecruiters.com/BoschGroup/hungary"
        self.variable_page_url = None
        self.page_counter = 0

        # Get data from user input data
        self.jobs = input_data["jobs"]
        self.search_location = input_data["search_location"]

        self.variable_page_url_changer()

    def run(self):
        try:
            if self.variable_page_url:
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
        has_job_content = True
        while has_job_content:
            self.variable_page_url_changer()
            soup = get_soup(self.variable_page_url)
            job_content_container = soup.html.body.find("div", class_="openings-body js-openings")
            has_job_content = bool(job_content_container.find("section", class_="openings-section opening opening--listed"))
            if has_job_content:
                for i in soup.html.body.find_all("a", class_="link--block details"):
                    job = str(i.h4.text).strip()
                    job_link = str(i["href"]).strip()
                    self.job.emit(get_data_dict(self.PORTAL_NAME, job, job_link))
                    for searched_job in self.jobs:
                        if searched_job in job.lower():
                            self.found_job.emit(get_data_dict(self.PORTAL_NAME, job, job_link))
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
        "Borsod-Abaúj-Zemplén megye":
            f"https://careers.smartrecruiters.com/BoschGroup/hungary?search=&page={page_counter}&location=Miskolc",
        "Budapest":
            f"https://careers.smartrecruiters.com/BoschGroup/hungary?search=&page={page_counter}&location=Budapest",
        "Heves megye":
            f"https://careers.smartrecruiters.com/BoschGroup/hungary?search=&page={page_counter}&location=Eger&location=Hatvan"
            f"&location=Maklár",
    }
