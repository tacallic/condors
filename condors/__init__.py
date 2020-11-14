import click
from .projectv2 import read_chick_assignments, location_updates, field_sites
from .pyped import PedFile


@click.command()
@click.argument('zims-file', type=click.Path(exists=True))
@click.option('-c', '--chicks', type=click.Path(exists=True), help='Chick Assignment File')
@click.option('-f', '--fws', type=click.Path(exists=True), help="FWS Living Birds File")
@click.option('-d', '--debug', is_flag=True)
@click.version_option(prog_name="Fischer")
def menu(zims_file,chicks=None, fws=None, debug=False):
    """
    Fischer's lovebird (Agapornis fischeri) is a small parrot species of the
     genus Agapornis. They were originally discovered in the late 19th century,
     and were first bred in the United States in 1926. They are named after
     German explorer Gustav Fischer.

    Unfortunately this is a computer program and isn't related to the birds at
     all. It's really too bad. They're cool birds.
     """

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
    ped_file = PedFile(zims_file)
    for individual in ped_file:
        # if the individual has a known location-change then do it
        if str(individual.Location) in location_updates:
            individual.Location = location_updates[str(individual.Location)]

    # print out the changes
    if debug:
        for individual in ped_file.get_modified_animals():
            print(individual)
            print(individual.modified_fields)
            print()

    # save the file
    new_ped_filename = f'mod_{zims_file}'
    new_ped_file = open(new_ped_filename, "w")
    new_ped_file.write(str(ped_file))

    # also new in 2020: want to see which birds need to be genotyped by comparing Cynthia's file
    # to the ZIMS living & released list
    # alive_zims = read_living_excel(ZIMS_living_released_file, 'alive & released')
    # genotyped_birds = read_genotype_excel(geno_filename)
    # data = add_genotypes(alive_zims,genotyped_birds)
    # added_genotypes_file = open("living_released_genotypes.txt", "w")
    # added_genotypes_file.write(str(data))

    # df = pd.DataFrame(data={"Condors with genotypes": data})
    # df.to_csv("living_released_genotypes.csv", sep="\t", index=False)

    print(f'{zims_file=} {chicks=} {fws=}')
    pass


def main():
    menu()
