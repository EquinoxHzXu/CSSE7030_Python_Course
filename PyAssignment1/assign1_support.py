
UNKNOWN_TEMP = 99999.9

def load_stations(stations_file):
    """Return the list of station names

    load_stations() -> list(str)
    """
    fd = open(stations_file, "r")
    stations = []
    for line in fd:
        line = line.strip()
        if not line:
            continue
        stations.append(line)
    fd.close()
    return stations


def display_temp(temp):
    """Display the temperature in an appropriate format. Dashes are displayed
    for invalid temperatures.

    display_temp(float) -> None
    """
    if temp == UNKNOWN_TEMP:
        print("{:<15}".format(" ----"), end='')
    else:
        print("{:<15}".format("{:5.1f}".format(temp)), end='')

def display_stations(stations, column0_name):
    """Displays a row of station names preceeded by column0_name.
    This is used as the heading for a table of data.

    display_stations(list(str), str) -> None
    """
    print("{:<12}".format(column0_name), end='')
    for s in stations:
        print("{:<15}".format(s), end='')
    print()



# For CSSE7030 students
def get_year_info(dates, start_year, end_year):
    """Return the list of years and list of indicies of the start of
    each year (including the index of the start of the year after end_year)

    get_year_info(list(str), str, str) -> (list(str), list(int))
    """
    years = [start_year]
    start_index = dates.index(start_year+"0101")
    indicies = [start_index]
    end_index = dates.index(end_year+"1231")
    year = int(start_year)
    for index in range(start_index+1, end_index):
        if dates[index].endswith("0101"):
            year += 1
            years.append(str(year))
            indicies.append(index)
    indicies.append(index+1)
    return (years, indicies)
