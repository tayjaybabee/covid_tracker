from datetime import datetime


def latest_timestamp(data):
    time_string_format = '%Y-%m-%dT%H:%M:%SZ'
    _new_time = datetime.strptime('2020-01-01T00:00:00Z', time_string_format)
    for state in data:
        state_timestamp = datetime.strptime(state['dateChecked'],
                                            time_string_format)  # example line from .yaml file: dateChecked: '2020-04-14T21:31:00Z'
        if state_timestamp > _new_time:
            _new_time = state_timestamp
    return _new_time
