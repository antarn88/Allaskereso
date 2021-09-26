from socket import error

from PySide2.QtCore import QThread, Signal
from bs4 import BeautifulSoup
from requests import get, post


class VMPWorker(QThread):
    error_msg = Signal(str, str, str)
    job = Signal(dict)
    found_job = Signal(dict)
    search_finished = Signal()

    def __init__(self, input_data):
        super(VMPWorker, self).__init__()

        # App attributes
        self.PORTAL_NAME = "Virtuális Munkaerőpiac Portál"
        self.PORTAL_URL = "https://vmp.munka.hu"
        self.soup_body = None
        self.variable_page_url = None
        self.error = False
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

    def is_the_page_available(self):
        return False if post(self.PORTAL_URL).status_code == 404 else True

    def get_jobs(self):
        blocked_on_site_text = "A portál átmenetileg hozzáférhetetlen az oldal korlátozásai miatt!"
        unavailable_jobs_text = "A portál szakszerűtlen programozása miatt nincsenek megjeleníthető állások!"
        has_next_page = True
        while has_next_page:
            if self.page_counter == 1:
                self.soup_body = get_soup(self.variable_page_url).body
            if not self.is_the_page_available():
                self.error = True
                self.error_msg.emit(self.PORTAL_NAME, blocked_on_site_text, self.variable_page_url)
                break
            if self.page_counter == 1:
                many_jobs_alert = bool(self.soup_body.find("div", class_="ui-widget"))
                if many_jobs_alert:
                    jobs_removed_empty_strings_list = list(filter(lambda item: item, self.jobs))
                    many_jobs_alert_text = self.soup_body.find("div", class_="ui-widget").li.text
                    if jobs_removed_empty_strings_list:
                        self.error_msg.emit(self.PORTAL_NAME, unavailable_jobs_text, self.variable_page_url)
                    else:
                        self.error_msg.emit(self.PORTAL_NAME, many_jobs_alert_text, self.variable_page_url)
                    break
            for result_line in self.soup_body.find("div", class_="baseFrame").findAll("tr"):
                for job_raw in result_line.select("td:first-child a"):
                    if str(job_raw["href"]).startswith("/allas/"):
                        job = str(job_raw.text).split(" - ", 1)[1].strip()
                        job_link = f'{self.PORTAL_URL}{str(job_raw["href"]).strip()}'
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
            active_page_location_li = 1
            for li in self.soup_body.find("ul", class_="pager").findAll("li"):
                if li.has_attr("class") and li["class"] == ["active"]:
                    break
                active_page_location_li += 1
            next_page_location_li = active_page_location_li + 1
            has_next_page = bool(self.soup_body.select(f".pager li:nth-child({next_page_location_li}) a"))
            if has_next_page:
                self.page_counter += 1
                self.variable_page_url_changer()
                self.soup_body = get_soup(self.variable_page_url).body
        if not self.is_the_page_available() and not self.error:
            self.error_msg.emit(self.PORTAL_NAME, blocked_on_site_text, self.variable_page_url)


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
            f"https://vmp.munka.hu/allas/talalatok?helyseg=B%C3%A1cs-Kiskun+megye&oldal={page_counter}",
        "Baranya megye":
            f"https://vmp.munka.hu/allas/talalatok?helyseg=Baranya+megye&oldal={page_counter}",
        "Békés megye":
            f"https://vmp.munka.hu/allas/talalatok?helyseg=B%C3%A9k%C3%A9s+megye&oldal={page_counter}",
        "Borsod-Abaúj-Zemplén megye":
            f"https://vmp.munka.hu/allas/talalatok?helyseg=Borsod-Aba%C3%BAj-Zempl%C3%A9n+megye&oldal={page_counter}",
        "Budapest":
            f"https://vmp.munka.hu/allas/talalatok?helyseg=Budapest&oldal={page_counter}",
        "Csongrád-Csanád megye":
            f"https://vmp.munka.hu/allas/talalatok?helyseg=Csongr%C3%A1d+megye&oldal={page_counter}",
        "Fejér megye":
            f"https://vmp.munka.hu/allas/talalatok?helyseg=Fej%C3%A9r+megye&oldal={page_counter}",
        "Győr-Moson-Sopron megye":
            f"https://vmp.munka.hu/allas/talalatok?helyseg=Gy%C5%91r-Moson-Sopron+megye&oldal={page_counter}",
        "Hajdú-Bihar megye":
            f"https://vmp.munka.hu/allas/talalatok?helyseg=Hajd%C3%BA-Bihar+megye&oldal={page_counter}",
        "Heves megye":
            f"https://vmp.munka.hu/allas/talalatok?helyseg=Heves+megye&oldal={page_counter}",
        "Jász-Nagykun-Szolnok megye":
            f"https://vmp.munka.hu/allas/talalatok?helyseg=J%C3%A1sz-Nagykun-Szolnok+megye&oldal={page_counter}",
        "Komárom-Esztergom megye":
            f"https://vmp.munka.hu/allas/talalatok?helyseg=Kom%C3%A1rom-Esztergom+megye&oldal={page_counter}",
        "Nógrád megye":
            f"https://vmp.munka.hu/allas/talalatok?helyseg=N%C3%B3gr%C3%A1d+megye&oldal={page_counter}",
        "Pest megye":
            f"https://vmp.munka.hu/allas/talalatok?helyseg=Pest+megye&oldal={page_counter}",
        "Somogy megye":
            f"https://vmp.munka.hu/allas/talalatok?helyseg=Somogy+megye&oldal={page_counter}",
        "Szabolcs-Szatmár-Bereg megye":
            f"https://vmp.munka.hu/allas/talalatok?helyseg=Szabolcs-Szatm%C3%A1r-Bereg+megye&oldal={page_counter}",
        "Tolna megye":
            f"https://vmp.munka.hu/allas/talalatok?helyseg=Tolna+megye&oldal={page_counter}",
        "Vas megye":
            f"https://vmp.munka.hu/allas/talalatok?helyseg=Vas+megye&oldal={page_counter}",
        "Veszprém megye":
            f"https://vmp.munka.hu/allas/talalatok?helyseg=Veszpr%C3%A9m+megye&oldal={page_counter}",
        "Zala megye":
            f"https://vmp.munka.hu/allas/talalatok?helyseg=Zala+megye&oldal={page_counter}"
    }
