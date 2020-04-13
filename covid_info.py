#!/usr/bin/env python3

"""

Python program to print out CoVid 19 data for the United States

"""

import requests
from argparse import ArgumentParser
from time import sleep
from datetime import datetime

parser = ArgumentParser('covid_info',
                        prefix_chars='+-',
                        add_help=True,
                        allow_abbrev=True, )

parser.add_argument('--gui', action='store_true', required=False,
                    help='Starts covid_tracker in graphical user interface mode',
                    dest='gui')

parser = parser.parse_args()

fetched = False


def fetch_data():
    """

    Grabs the latest data (retrieved from covidtracking.com) and returns the data
    sorted by most infected state to least infected state

    :return:
    """
    global fetched

    # API URL
    url = 'https://covidtracking.com/api/v1/states/current.json'

    # Get web results or print connection exception
    try:
        res = requests.get(url)
    except requests.exceptions.ConnectionError as e:
        print('Unable to reach data source. Please check your internet connection and try again!')
        exit(6)

    # Extract data from page
    data = res.json()

    # Sort data by total tested positive
    s_data = sorted(data, key=lambda d: d["positive"], reverse=True)

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


if parser.gui:
    print('')
    import PySimpleGUIQt as Qt

    layout = [
        [Qt.MultilineOutput(autoscroll=True, key='output')],
        [Qt.Button('Refresh', enable_events=True, key='refresh_bttn'),
         Qt.Button('Inspect', enable_events=True, key='inspect_bttn', visible=False),
         Qt.CloseButton('Close', key='close_bttn')]
    ]

    window = Qt.Window('CoVid 19 United States Stats', layout, size=(500, 600))
    print = window['output'].print

    while True:
        event, values = window.read(timeout=100)

        if not fetched:
            data = fetch_data()

        if fetched:
            window['inspect_bttn'].Update(visible=True)
            window.refresh()

        if event is None or event == 'close_bttn':
            window.close()
            exit()

        if event == 'refresh_bttn':
            fetched = False

        if event == 'inspect_bttn':
            Qt.PopupError('This feature is not yet implemented!', title='Not yet implemented!', keep_on_top=True)

fetch_data()
