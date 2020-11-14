class FieldSite:

    def __init__(self, name):
        self.FWS_individuals = []
        self.ZIMS_individuals = []
        self.name = name

    def __eq__(self, other_name):
        return self.name == other_name

    def __repr__(self):
        return str(self.name)

    def add_entry(self, bird, list_name):
        if list_name == "FWS":
            self.FWS_individuals.append(bird)
        if list_name == "ZIMS":
            self.ZIMS_individuals.append(bird)

    def add_zims_entry(self, bird_id):
        self.ZIMS_individuals.append(bird_id)

    def add_fws_entry(self, bird_id):
        self.FWS_individuals.append(bird_id)

    def find_unique_fws(self):
        fws_unique = []
        for bird in self.FWS_individuals:
            if bird not in self.ZIMS_individuals:
                fws_unique.append(bird)
        return fws_unique

    def find_unique_zims(self):
        zims_unique = []
        for bird in self.ZIMS_individuals:
            if bird not in self.FWS_individuals:
                zims_unique.append(bird)
        return zims_unique


