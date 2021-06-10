from parts.Database import Database


class InputData:
    def __init__(self, keywords, search_location, portals):
        self.keywords = keywords
        self.search_location = search_location
        self.portals = portals
        self.jobs = [job.strip().lower() for job in str(self.keywords).split(",")]
        self.db = Database(self.jobs, self.search_location, self.portals)

    def get_processed_data(self):
        return {
            "jobs": self.jobs,
            "search_location": self.search_location,
            "portals": self.portals
        }
