import click
import sys
import pandas as pd
from loguru import logger
from .projectv2 import read_chick_assignments, location_updates, field_sites, update_chicks, update_locations, read_steves_file, replace_location, populate_field_sites_zims, populate_field_sites_fws,fws_discrepancies_all_sites,zims_discrepancies_all_sites
from .pyped import PedFile
from .fieldsite import FieldSite

def setup_logging(log_level=None):
    logger.level("CUSTOM", no=15, color="<blue>", icon="@")
    logger.level("DEBUG", icon=r"D")
    logger.level("INFO", icon=r"I")
    logger.level("WARNING", icon=r"W")
    logger.level("ERROR", icon=r"E")
    if not log_level:
        log_level = 'INFO'
    else:
        log_level = log_level.upper()
    if log_level not in ['DEBUG', 'INFO', 'WARN', 'ERROR']:
        log_level = 'INFO'
    try:
        logger.remove(0)
        base_format = '{time:YYYYMMDD HH:mm:ss!UTC}Z [{level.icon}] ⋗ {message}'
        logger.add(sys.stdout, format=base_format, level=log_level)
    except ValueError:
        pass
    logger.debug(f'Logging Level Set To {log_level}')

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

    if debug:
        setup_logging('DEBUG')
    else:
        setup_logging('INFO')
    pass

    # New for 2020: we want to compare our living list to Steve's

    # First, read in the lists of ZIMS and FWS living birds & adjust locations to standard field site names.
    # alive_zims & alive_fws have the format [[bird ID, field site name], [bird ID, field site name]]

    # Second, go through list of birds and add them to the correct field sites.

    # Third, find birds that are unique to each list (discrepancies) and write them to a file.
    #
    # # Next, we want to correct the zims file with field site names
    ped_file = PedFile(zims_file)

    if fws:
        alive_zims = ped_file.get_zims_living()
        alive_fws = read_steves_file(fws)
        replace_location(alive_fws)

        cali = FieldSite("WILD-CA")
        baja = FieldSite("WILD-BAJA")
        ariz = FieldSite("WILD-AZ")

        field_sites = [cali, baja, ariz]

        field_sites = populate_field_sites_zims(alive_zims, field_sites)
        field_sites = populate_field_sites_fws(alive_fws, field_sites)

        problems_output = []
        fws_problems = fws_discrepancies_all_sites(alive_zims, field_sites)
        zims_problems = zims_discrepancies_all_sites()
        problems_output = problems_output + fws_problems + zims_problems

        df = pd.DataFrame(data={"Data Discrepancies": problems_output})
        df.to_csv(discrepancy_out_filename, sep=",", index=False)

    if chicks:
        logger.debug("Chick file supplied, updating chicks")
        ped_file = update_chicks(ped_file, chicks)

    ped_file = update_locations(ped_file)

    # print out the changes
    for individual in ped_file.get_modified_animals():
        logger.debug(f'MODIFIED ANIMAL {individual.GAN}')
        logger.debug(individual.modified_fields)
        logger.debug("--")
    # save the file
    new_ped_filename = f'mod_{zims_file}'
    logger.debug(f"saving output to {new_ped_filename}")
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
