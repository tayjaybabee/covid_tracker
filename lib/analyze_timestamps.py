from datetime import datetime

def latestTimeStamp(data):
    time_string_format = '%Y-%m-%dT%H:%M:%SZ'
    newesttimestamp = datetime.strptime('2020-01-01T00:00:00Z', time_string_format)
    for state in data:
        state_timestamp = datetime.strptime(state['dateChecked'], time_string_format) # example line from .yaml file: dateChecked: '2020-04-14T21:31:00Z'
        if state_timestamp > newesttimestamp:
            newesttimestamp = state_timestamp
    return newesttimestamp

