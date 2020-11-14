class PedFile:

    individuals = []

    header = ""
    footer = ""

    def __init__(self, filename):
        self.ped_source = open(filename, "r")
        for line in self.ped_source:
            line = line.rstrip()
            if line.startswith("ID") or line.startswith("*SIRE") or line.startswith("*DAM"):
                self.footer += line + "\n"
                continue
            if line.startswith("*") or line.startswith("Number") or line.startswith("StudbookID") or len(line) == 0:
                self.header += line + "\n"
                continue
            self.individuals.append(Individual(line))

    def __iter__(self):
        for individual in self.individuals:
            yield individual

    def __str__(self):
        write_me = ""
        write_me += self.header
        for animal in self.individuals:
            write_me += str(animal) + "\n"
        write_me += self.footer
        return write_me

    def get_modified_animals(self):
        for individual in self.individuals:
            if individual.modified:
                yield individual

    def get_unmodified_animals(self):
        for individual in self.individuals:
            if not individual.modified:
                yield individual

    def get_zims_living(self):
        results = []
        for individual in self.individuals:
            if not individual.Dead:
                bird_id = individual.GAN
                bird_location = individual.Location
                bird_data = [bird_id, bird_location]
                results.append(bird_data)
        return results


class Individual:

    modified = False
    modified_fields = []

    def __init__(self, line):
        elements = line.split(";")
        self.GAN = self._GANData(elements[0])
        self.Sire = self._SireData(elements[1])
        self.Dam = self._DamData(elements[2])
        self.Sex = self._SexData(elements[3])
        self.GenSelected = self._GenSelectedData(elements[4])
        self.DemSelected = self._DemSelectedData(elements[5])
        self.Dead = self._DeadData(elements[6])
        self.BirthDate = self._PEDDate(elements[7])
        self.DeathDate = self._PEDDate(elements[8])
        self.Location = self._LocationData(elements[9])
        self.LocalID = self._LocalIDData(elements[10])
        self.HouseName = self._HouseNameData(elements[11])
        self.Number = self._NumberData(elements[12])
        self.Tags = self._TagsData(elements[13])
        self.Bands = self._BandsData(elements[14])
        self.Transponders = self._TranspondersData(elements[15])
        self.Rearing = self._RearingData(elements[16])
        self.BirthType = self._BirthTypeData(elements[17])
        self.BirthLocation = self._BirthLocationData(elements[18])
        self.Contraception = self._ContraceptionData(elements[19])
        self.Taxonomy = self._TaxonomyData(elements[20])
        self.ConceptionDate = self._ConceptionDateData(elements[21])
        self.Association = self._AssociationData(elements[22])
        self.UDFLASTSEEN = self._UDFLASTSEENData(elements[23])
        self.UDFCLAN = self._UDFCLANData(elements[24])
        self.UDFRELSITE = self._UDFRELSITEData(elements[25])
        self.modified = False
        self.modified_fields = list()

    def __str__(self):
        write_me = ""
        write_me += repr(self.GAN) + ";"
        write_me += repr(self.Sire) + ";"
        write_me += repr(self.Dam) + ";"
        write_me += repr(self.Sex) + ";"
        write_me += repr(self.GenSelected) + ";"
        write_me += repr(self.DemSelected) + ";"
        write_me += repr(self.Dead) + ";"
        write_me += repr(self.BirthDate) + ";"
        write_me += repr(self.DeathDate) + ";"
        write_me += repr(self.Location) + ";"
        write_me += repr(self.LocalID) + ";"
        write_me += repr(self.HouseName) + ";"
        write_me += repr(self.Number) + ";"
        write_me += repr(self.Tags) + ";"
        write_me += repr(self.Bands) + ";"
        write_me += repr(self.Transponders) + ";"
        write_me += repr(self.Rearing) + ";"
        write_me += repr(self.BirthType) + ";"
        write_me += repr(self.BirthLocation) + ";"
        write_me += repr(self.Contraception) + ";"
        write_me += repr(self.Taxonomy) + ";"
        write_me += repr(self.ConceptionDate) + ";"
        write_me += repr(self.Association) + ";"
        write_me += repr(self.UDFLASTSEEN) + ";"
        write_me += repr(self.UDFCLAN) + ";"
        write_me += repr(self.UDFRELSITE)

        return write_me

    def __setattr__(self, name, value):
        # if this is being modified by a user (as a string or boolean) then we record it as a change
        if isinstance(value, (bool, str)) and name != "modified" and name != "modified_fields":
            if bool(self.__dict__[name]) == value or str(self.__dict__[name]) == value:
                pass
            else:
                self.modified_fields.append({"attribute": name, "to": str(value), "from": str(self.__dict__[name])})
                self.modified = True
                self.__dict__[name] = getattr(self, "_" + name + "Data")(value)
        # if this is a new object then we just assign it without recording a change
        else:
            self.__dict__[name] = value

    # super-class for Dead and Selected classes
    class _TrueOrFalse(object):
        data = ""

        def __init__(self, inp):
            self.data = self.normalize_input(inp)

        def set_state(self, inp):
            self.data = self.normalize_input(inp)

        def get_state(self):
            return self.data

        def __str__(self):
            if self.data:
                return "True"
            return "False"

        def __repr__(self):
            if self.data:
                return "T"
            return "F"

        def __bool__(self):
            return self.data

        @staticmethod
        def normalize_input(inp):
            if isinstance(inp, bool):
                return inp
            elif isinstance(inp, str):
                raw = inp.strip().upper()
                if raw == "T":
                    return True
                elif raw == "F":
                    return False
                else:
                    raise ValueError("Bad data found in 'dead' field: " + raw)
            else:
                raise ValueError("Bad data found in 'dead' field!")

    # super-class defining most everything necessary for data, defaulting to a field width of 10
    class _PEDBasic(object):
        data = ""
        field_len = 14

        def __init__(self, inp):
            self.data = inp.strip()

        def __str__(self):
            return self.data

        def __repr__(self):
            return self.data.rjust(self.field_len, ' ')[:self.field_len]

    class _GANData(_PEDBasic):
        field_len = 10

    class _SireData(_PEDBasic):
        field_len = 10

    class _DamData(_PEDBasic):
        field_len = 10

    class _SexData(_PEDBasic):
        field_len = 1

    class _GenSelectedData(_TrueOrFalse):
        field_len = 1

    class _DemSelectedData(_TrueOrFalse):
        field_len = 1

    class _DeadData(_TrueOrFalse):
        field_len = 1

    class _PEDDate(_PEDBasic):
        field_len = 8

    class _LocationData(_PEDBasic):
        field_len = 10

        def __repr__(self):
            return self.data.ljust(self.field_len, ' ')[:self.field_len]

    class _LocalIDData(_PEDBasic):
        field_len = 6

        def __repr__(self):
            return self.data.ljust(self.field_len, ' ')[:self.field_len]

    class _HouseNameData(_PEDBasic):
        field_len = 14

    class _NumberData(_PEDBasic):
        field_len = 14

    class _TagsData(_PEDBasic):
        field_len = 14

    class _BandsData(_PEDBasic):
        field_len = 8

    class _TranspondersData(_PEDBasic):
        field_len = 14

    class _RearingData(_PEDBasic):
        field_len = 7

    class _BirthTypeData(_PEDBasic):
        field_len = 7

    class _BirthLocationData(_PEDBasic):
        field_len = 10

    class _ContraceptionData(_PEDBasic):
        field_len = 4

    class _TaxonomyData(_PEDBasic):
        field_len = 20

    class _ConceptionDateData(_PEDDate):
        field_len = 10

    class _AssociationData(_PEDBasic):
        field_len = 10

    class _UDFLASTSEENData(_PEDDate):
        field_len = 10

    class _UDFCLANData(_PEDBasic):
        field_len = 4

    class _UDFRELSITEData(_PEDBasic):
        field_len = 10


