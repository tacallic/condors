import sys
import xlrd
import pandas as pd
from .pyped import PedFile
from .fieldsite import FieldSite

# chick_assignments = dict()

ped_filename = "zims10-15-2020.zims"
chick_assignments_filename = "input.xlsx"

update_from_filename = "ZIMSlivingreleased6-25-2019.txt"
ZIMS_living_released_file = "ZIMS Lists 2-7-2020.xlsx"

FWS_file = "Jan. 2020 living.xlsx"

geno_filename = "Chondro_genotypes_short.xlsx"


new_ped_filename = "output10-15-2020.zims"
discrepancy_out_filename = "discrepancy_birds.csv"

location_updates = {
    "BITTER CK": "WILD-CA",
    "HOPPER": "WILD-CA",
    "PACINES": "WILD-CA",
    "PAICINES": "WILD-CA",
    "PACAINES": "WILD-CA",
    "VENTANA": "WILD-CA",
    "SPM SITE": "WILD-BAJA",
    "STEINMETZ": "WILD-AZ",
    "LIBERTY W": "WILD-AZ",
    "WILD-UT": "WILD-AZ",
    "VERMILION": "WILD-AZ",
    "SOCAL ALIVE": "WILD-CA",
    "AZ ALIVE": "WILD-AZ",
    "PNP": "WILD-CA",
    "BAJA": "WILD-BAJA",
    "SD-WAP": "CAPTIVE",
    "OAKLAND": "CAPTIVE",
    "PHOENIX": "CAPTIVE",
    "PORTLAND": "CAPTIVE",
    "CA LIV MU": "CAPTIVE",
    "LOSANGELE": "CAPTIVE",
    "MEXICOCTY": "CAPTIVE",
    "PEREGPROP": "CAPTIVE",
    "S BARBARA": "CAPTIVE",
    "SANDIEGOZ": "CAPTIVE"
}


def read_chick_assignments(filename: str):
    df = pd.read_excel(filename)
    chick_assignments = dict()
    for index, row in df.iterrows():
        bird_id = str(row['ID'])
        bird_location = str(row['Location']).upper().strip()
        chick_assignments[bird_id] = bird_location
    return chick_assignments

# region Methods/Functions
# To read in just a list of living bird IDs from a text file
def read_living_txt(update_txt_file):
    update_from_file = open(update_txt_file, "r")
    living_birds = []
    for line in update_from_file:
        living_birds.append(line.rstrip())
    return living_birds


# To read in Steve's 2020 list of living wild birds from excel
def read_steves_file(steves_file):
    wild_file = xlrd.open_workbook(steves_file)
    data = wild_file.sheet_by_index(0)
    fws_birds = []
    current_location = ""
    for value in data.col_values(0):
        if isinstance(value, str):
            current_location = value.upper().strip()
        if isinstance(value, float):
            current_bird = int(value)
            bird_data = [current_bird, current_location]
            fws_birds.append(bird_data)
    return fws_birds


# To read in Cynthia's list of birds that have been genotyped.
# Returns a list of lists [[bird id, bird genotype], [bird id, bird genotype]]
def read_genotype_excel(genotype_file):
    geno_birds = []
    data = pd.read_excel(genotype_file)
    for index, row in data.iterrows():
        bird_id = int(row['Studbook ID'])
        bird_genotype = str(row['Status'])
        bird_data = [bird_id, bird_genotype]
        geno_birds.append(bird_data)
    return geno_birds


# To read in living&released bird IDs and locations in ZIMS Export Individuals format
def read_living_excel(update_xlsx_file, sheet):
    df = pd.read_excel(update_xlsx_file, sheet_name=sheet)
    zims_birds = []
    for index, row in df.iterrows():
        bird_id = int(row['Studbook ID'])
        bird_location = str(row['Current Location']).upper().strip()
        bird_data = [bird_id, bird_location]
        zims_birds.append(bird_data)
    return zims_birds


# Takes a list of lists [[bird ID, location], [bird ID, location]] and replaces locations with location_updates
def replace_location(bird_list):
    global location_updates
    for bird in bird_list:
        if bird[1] in location_updates:
            bird[1] = location_updates[str(bird[1])]
    return bird_list


# Takes a list of living birds from ZIMS [[bird ID, field site name], [bird ID, field site name]] and assigns birds
# to Field Sites
def populate_field_sites_zims(zims_list, field_sites):
    for bird in zims_list:
        for site in field_sites:
            if bird[1] == site:
                site.add_zims_entry(bird[0])
    return field_sites


# Takes a list of living birds from FWS [[bird ID, field site name], [bird ID, field site name]] and assigns birds
# to Field Sites
def populate_field_sites_fws(fws_list, field_sites):
    for bird in fws_list:
        for site in field_sites:
            if bird[1] == site:
                site.add_fws_entry(bird[0])
    return field_sites

# Takes the list of ZIMS living & released birds and adds their genotype info from genotype file
def add_genotypes(living_list, geno_list):
    genotypes_added = []
    for ZIMS_bird in living_list:
        for geno_bird in geno_list:
            if ZIMS_bird[0] == geno_bird[0]:
                ZIMS_bird.append(geno_bird[1])
                # print(str(ZIMS_bird[0]) + " " + str(geno_bird[0]))
        genotypes_added.append(ZIMS_bird)
    return genotypes_added


# Calls discrepancy functions for all field sites to find birds unique to FWS list, then tries to find them in ZIMS
# data. Returns a list of the discrepancies.
def fws_discrepancies_all_sites(alive_zims, field_sites):
    discrepancy_list = []
    for site in field_sites:
        fws_birds = site.find_unique_fws()
        discrepancy_list = discrepancy_list + fws_birds
    for_output = []
    for fws_bird in discrepancy_list:
        discrepancy_found = False
        for zims_bird in alive_zims:
            if zims_bird[0] == fws_bird:  # zims_bird[0] is bird ID
                for_output.append(str(zims_bird[0]) + " ZIMS Location: " + zims_bird[1])
                discrepancy_found = True
                break
        if not discrepancy_found:
            for_output.append(str(fws_bird) + " not in ZIMS alive/released")
    return for_output


# Calls discrepancy functions for all field sites to find birds unique to ZIMS list, then tries to find them in FWS
# data. Returns a list of the discrepancies.
def zims_discrepancies_all_sites(alive_fws,field_sites):
    discrepancy_list = []
    for site in field_sites:
        zims_birds = site.find_unique_zims()
        discrepancy_list = discrepancy_list + zims_birds
    for_output = []
    for zims_bird in discrepancy_list:
        discrepancy_found = False
        for fws_bird in alive_fws:
            if fws_bird[0] == zims_bird:  # fws_bird[0] is bird ID
                for_output.append(str(fws_bird[0]) + " Location: " + fws_bird[1])
                discrepancy_found = True
                break
        if not discrepancy_found:
            for_output.append(str(zims_bird) + " not in FWS alive")
    return for_output


# Used in 2019 analysis to change Dem and Gen selected status based on a list of living birds, and to apply location
# updates and to 'move' 2018 chicks to their final release sites. In 2020 we'll use PMx Selection tab to update Dem
# and Gen selected status.
def update_chicks(ped_file: PedFile, chick_file: str):
    #alive_birds = read_living_txt(update_from_filename)
    # ped_file = PedFile(ped_filename)

    chick_assignments = read_chick_assignments(chick_file)

    for individual in ped_file:

        # if the GAN is in our list then make sure it matches what we want
        # if str(individual.GAN) in alive_birds:
        #     individual.DemSelected = True
        #     individual.GenSelected = True
        #     individual.Dead = False

        # if the individual has a known location-change then do it
        # if str(individual.Location) in location_updates:
        #     individual.Location = location_updates[str(individual.Location)]

        # if it's a 2018 chick, 'move' it to its release site
        if str(individual.GAN) in chick_assignments:
            individual.Location = chick_assignments[str(individual.GAN)]

    return ped_file


def update_locations(ped_file: PedFile):
    for individual in ped_file:
        # if the individual has a known location-change then do it
        if str(individual.Location) in location_updates:
            individual.Location = location_updates[str(individual.Location)]
    return ped_file

# endregion


# New for 2020: we want to compare our living list to Steve's

# First, read in the lists of ZIMS and FWS living birds & adjust locations to standard field site names.
# alive_zims & alive_fws have the format [[bird ID, field site name], [bird ID, field site name]]
# alive_zims = read_living_excel(ZIMS_living_released_file, 'alive & released')
# alive_fws = read_steves_file(FWS_file)
# replace_location(alive_fws)
# replace_location(alive_zims)

# Second, go through list of birds and add them to the correct field sites.
# populate_field_sites_zims(alive_zims)
# populate_field_sites_fws(alive_fws)

# Third, find birds that are unique to each list (discrepancies) and write them to a file.
# problems_output = []
# fws_problems = fws_discrepancies_all_sites()
# zims_problems = zims_discrepancies_all_sites()
# problems_output = problems_output + fws_problems + zims_problems
#
# df = pd.DataFrame(data={"Data Discrepancies": problems_output})
# df.to_csv(discrepancy_out_filename, sep=",", index=False)
#
# # Next, we want to correct the zims file with field site names
# ped_file = pyped.PedFile(ped_filename)
# for individual in ped_file:
#     # if the individual has a known location-change then do it
#     if str(individual.Location) in location_updates:
#         individual.Location = location_updates[str(individual.Location)]
#
# # print out the changes
# for individual in ped_file.get_modified_animals():
#     print(individual)
#     print(individual.modified_fields)
#     print()
#
# # save the file
# new_ped_file = open(new_ped_filename, "w")
# new_ped_file.write(str(ped_file))

# also new in 2020: want to see which birds need to be genotyped by comparing Cynthia's file
# to the ZIMS living & released list
# alive_zims = read_living_excel(ZIMS_living_released_file, 'alive & released')
# genotyped_birds = read_genotype_excel(geno_filename)
# data = add_genotypes(alive_zims,genotyped_birds)
# added_genotypes_file = open("living_released_genotypes.txt", "w")
# added_genotypes_file.write(str(data))

# df = pd.DataFrame(data={"Condors with genotypes": data})
# df.to_csv("living_released_genotypes.csv", sep="\t", index=False)

# print("done!")
# sys.exit(0)
