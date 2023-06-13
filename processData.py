import csv
from datetime import datetime, timedelta
from dateutil import parser
from collections import defaultdict

def lateral_g_force(x, y):
    return (x ** 2 + y ** 2) ** 0.5


# for the purpose of the demo, we are using a set person's name. In prod we would have the endpoints identify themselves.
NAME = "KEVIN"

# dictionary to hold the result
occurrences = defaultdict(int)

# initial time offset
time_offset = 0

# array to hold exceedances
exceedances = []

import datetime

def parse_time(time_str):
    date, time = time_str.split("@")
    year, month, day = map(float, date.split("-"))
    hour, minute, second = map(float, time.split(":"))
    return datetime.datetime(int(year), int(month), int(day), int(hour), int(minute), int(second))




def getViolations():
    global time_offset
    global NAME
    with open(f'{NAME}.csv', 'r') as file:
        reader = csv.reader(file)
        start_time = None
        for row in reader:
            if row[0].startswith('++++'):
                time_offset = float(row[1])
            else:
                # parse time, add the offset
                timestamp = parse_time(row[0])
                timestamp = timestamp + datetime.timedelta(seconds=time_offset - 86400)
                g_force = float(row[3])
                lateral_g = lateral_g_force(float(row[1]), float(row[2]))

                if start_time is None and (g_force > 0.2 or lateral_g > 0.1):
                    start_time = timestamp
                elif start_time is not None and (g_force <= 0.2 and lateral_g <= 0.2):
                    diff = timestamp - start_time
                    if diff.total_seconds() > 2:
                        print(f"Exceeded 0.2gs from {start_time} to {timestamp}")
                        occurrences[start_time.date()] += 1
                    start_time = None
                    # reset exceedances
                    exceedances = []

    # handle the last batch of exceedances
    if exceedances and (exceedances[-1] - exceedances[0]).total_seconds() > 2:
        date_key = exceedances[0].date().isoformat()
        if date_key in occurrences:
            occurrences[date_key] += 1
        else:
            occurrences[date_key] = 1

    # how many violations
    print(sum([i for i in occurrences.values()]))

    # return {  str(start_time.date()):sum([i for i in occurrences.values()])}
    return (str(start_time.date()), NAME, sum([i for i in occurrences.values()])) # for the purpose of the demo, we are using a set person's name. In prod we would have the endpoints identify themselves.

print(getViolations())