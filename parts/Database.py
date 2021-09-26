from sqlite3 import connect


class Database:
    def __init__(self, jobs=None, exclude_words=None, location=None, portals=None):

        # App attributes
        self.conn = None
        self.curs = None

        self.create_database()
        self.create_tables()

        if not self.get_locations():
            self.set_locations()

        if jobs:
            self.set_jobs(jobs)

        if exclude_words:
            self.set_exclude_words(exclude_words)

        if location:
            self.set_location(location)

        if not self.get_supported_portals():
            self.set_supported_portals()

        if portals:
            self.set_portals(portals)

    def create_database(self):
        self.conn = connect("data.db")

    def create_tables(self):
        self.curs = self.conn.cursor()
        self.curs.execute("CREATE TABLE IF NOT EXISTS keresett_allasok (allas TEXT)")
        self.curs.execute("CREATE TABLE IF NOT EXISTS preferalt_regio (regio TEXT)")
        self.curs.execute("CREATE TABLE IF NOT EXISTS regiok (regio TEXT)")
        self.curs.execute("CREATE TABLE IF NOT EXISTS preferalt_portalok (portal TEXT)")
        self.curs.execute("CREATE TABLE IF NOT EXISTS tamogatott_portalok (portal TEXT)")
        self.curs.execute("CREATE TABLE IF NOT EXISTS kizart_kulcsszavak (szo TEXT)")

    def get_searched_jobs_from_db(self):
        self.curs.execute("SELECT allas FROM keresett_allasok")
        return [job[0] for job in self.curs.fetchall()]

    def get_exclude_words_from_db(self):
        self.curs.execute("SELECT szo FROM kizart_kulcsszavak")
        return [word[0] for word in self.curs.fetchall()]

    def get_searched_jobs_from_db_str(self):
        return ", ".join(self.get_searched_jobs_from_db()).strip()

    def get_exclude_words_from_db_str(self):
        return ", ".join(self.get_exclude_words_from_db()).strip()

    def clear_tables(self):
        self.curs.execute("DELETE FROM keresett_allasok")
        self.curs.execute("DELETE FROM preferalt_regio")
        self.curs.execute("DELETE FROM preferalt_portalok")
        self.curs.execute("DELETE FROM kizart_kulcsszavak")

    def set_jobs(self, jobs):
        self.clear_tables()

        for job in jobs:
            job = job.lower().strip()
            if job not in self.get_searched_jobs_from_db():
                self.curs.execute(f"INSERT INTO keresett_allasok VALUES ('{job}')")
        self.conn.commit()

    def set_exclude_words(self, words):
        for word in words:
            word = word.lower().strip()
            if word not in self.get_exclude_words_from_db():
                self.curs.execute(f"INSERT INTO kizart_kulcsszavak VALUES ('{word}')")
        self.conn.commit()

    def set_location(self, location):
        self.curs.execute(f"INSERT INTO preferalt_regio VALUES ('{location}')")
        self.conn.commit()

    def get_location(self):
        self.curs.execute("SELECT regio FROM preferalt_regio")
        try:
            return [job[0] for job in self.curs.fetchall()][0]
        except IndexError:
            return None

    def set_locations(self):
        locations = ["Bács-Kiskun megye", "Baranya megye", "Békés megye", "Borsod-Abaúj-Zemplén megye", "Budapest",
                     "Csongrád-Csanád megye", "Fejér megye", "Győr-Moson-Sopron megye", "Hajdú-Bihar megye", "Heves megye", "Jász-Nagykun-Szolnok megye",
                     "Komárom-Esztergom megye", "Nógrád megye", "Pest megye", "Somogy megye", "Szabolcs-Szatmár-Bereg megye", "Tolna megye", "Vas megye",
                     "Veszprém megye", "Zala megye"]

        [self.curs.execute(f"INSERT INTO regiok VALUES ('{location}')") for location in locations]
        self.conn.commit()

    def get_locations(self):
        self.curs.execute("SELECT regio FROM regiok")
        return [job[0] for job in self.curs.fetchall()]

    def set_portals(self, portals):
        [self.curs.execute(f"INSERT INTO preferalt_portalok VALUES ('{portal}')") for portal in portals]
        self.conn.commit()

    def get_portals(self):
        self.curs.execute("SELECT portal FROM preferalt_portalok")
        return [job[0] for job in self.curs.fetchall()]

    def set_supported_portals(self):
        supported_portals = ["Mindegyik/egyik sem",
                             "Profession (profession.hu)",
                             # "Evosoft (evosoft.hu)",
                             "Bosch (bosch.hu)",
                             "Állás.Club (allas.club)",
                             "Virtuális Munkaerőpiac Portál (vmp.munka.hu)",
                             # "Jobmonitor (jobmonitor.hu)",
                             "ÉRV (ervzrt.hu)",
                             "Cvonline (cvonline.hu)",
                             "Humán Centrum (humancentrum.hu)",
                             "Pannonwork (allas.pannonwork.hu)",
                             "Közigállás (kozigallas.gov.hu)",
                             "Borsodchem (karrier.borsodchem.eu)"]

        [self.curs.execute(f"INSERT INTO tamogatott_portalok VALUES ('{portal}')") for portal in supported_portals]
        self.conn.commit()

    def get_supported_portals(self):
        self.curs.execute("SELECT portal FROM tamogatott_portalok")
        return [job[0] for job in self.curs.fetchall()]
