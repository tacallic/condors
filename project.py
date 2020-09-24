import sys
import re
import pyped

ped_filename = "originalPed.ped"
update_from_filename = "sorted"

dead_bird_regex = ".*[T|F];F;[0-9]*;.*"
dead_bird_checker = re.compile(dead_bird_regex)

new_ped_filename = "output.ped"
new_ped_file = open(new_ped_filename, "w")

#location is field 8
location_updates = {
    "BITTER CK": "WILD-CA",
    "HOPPER": "WILD-CA",
    "PACINES": "WILD-CA",
    "PAICINES": "WILD-CA",
    "VENTANA": "WILD-CA",
    "SPM SITE": "WILD-BAJA",
    "STEINMETZ": "WILD-AZ",
    "WILD-UT": "WILD-AZ",
    "VERMILION": "WILD-AZ"
}

# first, we're going to make a list of wild birds known to be alive
update_from_file = open(update_from_filename, "r")
wild_birds = []
for line in update_from_file:
    wild_birds.append(line.rstrip())


counter = 0
header_lines = 0
other_lines = 0
ok_lines = 0
bad_lines = 0
ped_file = open(ped_filename, "r")
for line in ped_file:
    line = line.rstrip()

    # if we're in the header, just print it out and continue
    if line.startswith("*") or line.startswith("Number") or len(line) == 0:
        header_lines +=1
        new_ped_file.write(line + "\n")
        continue

    # make sure everything is uppercase from here on out
    line = line.upper()

    # grab the bird_id from the line, this is what will match in wild_birds
    elements = line.split(";")
    bird_id = elements[0].strip()

    # if the bird_id isn't in wild_birds we can just print the line
    if bird_id not in wild_birds:
        other_lines +=1
        new_ped_file.write(line + "\n")
        continue

    selected = True if elements[4] == "T" else False
    dead = True if elements[5] == "T" else False

    # want end state to be:
    #  dead == False
    #  selected == True

    # if we already have the correct state then we can just print and move on
    if not dead and selected:
        ok_lines += 1
        new_ped_file.write(line + "\n")
        continue

    # lastly, we need to update the line to show dead==false && selected==true
    elements[4] = "F"
    elements[5] = "T"

    write_me = ""
    for element in elements:
        write_me += element + ";"

    bad_lines += 1
    write_me = write_me[:-1]

    new_ped_file.write(write_me + "s\n")

print(f"other lines: {other_lines}")
print(f"ok lines: {ok_lines}")
print(f"bad lines: {bad_lines}")
print(f"header lines: {header_lines}")
print(f"total lines in file: {ok_lines + bad_lines + header_lines + other_lines}")
print()
print(f"TOTAL BIRDS: {ok_lines + bad_lines + other_lines}")
sys.exit(0)
