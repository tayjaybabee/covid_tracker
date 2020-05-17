from datetime import datetime
from pathlib import Path

import requests
import yaml

from lib.analyze_timestamps import latest_timestamp

fetched = False

def fetch_data(gui=False, **kwargs):
    """

    Grabs the latest data (retrieved from covidtracking.com) and returns it line-by-line sorted by most infected state
    to least infected state

    :return: dict
    """
    global fetched, print

    if 'main_win' in kwargs.keys():
        print = kwargs['main_win'].print
    else:
        print = print


    # API URL
    url = 'https://covidtracking.com/api/v1/states/current.json'
    should_read = False

    data = []

    yaml_dbname = 'data.yaml'
    if Path(yaml_dbname).exists():
        current_time = datetime.now()
        yaml_db_filepath = open(yaml_dbname, 'rt')
        data = yaml.safe_load(yaml_db_filepath.read())
        yaml_db_filepath.close()
        # should_read=False
        import_timestamp = latest_timestamp(data)
        age_seconds = (current_time - import_timestamp).total_seconds()
        if age_seconds > 21600:
            should_read = True  # file too old
        else:
            should_read = False  # file recent; don't hit up the web server this time
    else:
        should_read = True  # file not found; retrieve data from web server and save it to the file

    if should_read:
        # Get web results or print connection exception
        try:
            res = requests.get(url)
            should_read = True

            # Extract data from page
            data = res.json()
        except requests.exceptions.ConnectionError as e:
            print('Unable to reach data source. Please check your internet connection and try again!')
            should_read = False
            exit(6)

    # Sort data by total tested positive
    s_data = sorted(data, key=lambda d: d["positive"], reverse=True)

    if should_read:
        db_out_filename = 'data.yaml'
        db_out = open(db_out_filename, 'wt')
        db_out.write(yaml.dump(s_data))
        db_out.close()

    # Set up accumulators for important stats delivered after sorted results
    total_infected = 0
    total_dead = 0
    total_recovered = 0

    # Iterate through the data and perform the needed operations on it
    for state in s_data:
        pos = state['positive']

        # Add commas to 'positive' field
        f_pos = "{:,}".format(pos)

        # Add state's infected to total
        total_infected += pos

        # Grab the state's name
        name = state['state']

        # Grab the total amount recovered
        recovered = state['recovered']

        # Add commas to 'recovered' amount if it's not None, and add this state's total to the grand total
        if recovered is not None:
            f_recovered = "{:,}".format(recovered)
            total_recovered += recovered
        else:
            f_recovered = recovered

        # Grab the total deceased
        deceased = state['death']

        if deceased is not None:
            # Add commas to 'deceased' amount
            f_deceased = "{:,}".format(deceased)

            # Add state's number to total
            total_dead += deceased

        # Prepare statement to print for the state totals and then print it
        statement = str(f"{name}: Infected: {f_pos} | Recovered: {f_recovered} | Deceased: {f_deceased}")
        print(statement)

    # Format stat totals
    f_total_infected = "{:,}".format(total_infected)
    f_total_dead = "{:,}".format(total_dead)
    f_total_recovered = "{:,}".format(total_recovered)

    # Prepare totals statement and print it
    total_statement = str(
        f'Total Infected: {f_total_infected} | Total Recovered: {f_total_recovered} | Total Dead: {f_total_dead}')
    print(total_statement)
    fetched = True

    last_fetched = datetime.now()
    lf_str = last_fetched.strftime("%d/%m/%Y %H:%M:%S")
    lf_statement = f'Last fetched: {lf_str}'
    print(lf_statement)

    return s_data
