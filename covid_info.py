"""

Python program to print out CoVid 19 data for the United States

"""

import requests

# API URL
url = 'https://covidtracking.com/api/v1/states/current.json'

# Get web results
res = requests.get(url)

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

    # Add state's number to total
    total_dead += deceased

    # Add commas to 'deceased' amount
    f_deceased = "{:,}".format(deceased)

    # Prepare statement to print for the state totals and then print it
    statement = str(f"{name}: Infected: {f_pos} | Recovered: {f_recovered} | Deceased: {f_deceased}")
    print(statement)

# Format stat totals
f_total_infected = "{:,}".format(total_infected)
f_total_dead = "{:,}".format(total_dead)
f_total_recovered = "{:,}".format(total_recovered)

# Prepare totals statement and print it
total_statement = str(f'Total Infected: {f_total_infected} | Total Recovered: {f_total_recovered} | Total Dead: {f_total_dead}')
print(total_statement)


