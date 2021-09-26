from parts.Database import Database


class InputData:
    def __init__(self, keywords, exclude_words, search_location, portals):
        self.keywords = keywords
        self.exclude_words = exclude_words
        self.search_location = search_location
        self.portals = portals
        self.jobs = [job.strip().lower() for job in str(self.keywords).split(",")]
        self.exc_words = [word.strip().lower() for word in str(self.exclude_words).split(",")]
        self.db = Database(self.jobs, self.exc_words, self.search_location, self.portals)

    def get_processed_data(self):
        return {
            "jobs": self.jobs,
            "exclude_words": self.exc_words,
            "search_location": self.search_location,
            "portals": self.portals
        }
