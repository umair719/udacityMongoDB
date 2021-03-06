__author__ = 'Umair'


# -*- coding: utf-8 -*-
# Find the time and value of max load for each of the regions
# COAST, EAST, FAR_WEST, NORTH, NORTH_C, SOUTHERN, SOUTH_C, WEST
# and write the result out in a csv file, using pipe character | as the delimiter.
# An example output can be seen in the "example.csv" file.

import xlrd
import os
import csv
from zipfile import ZipFile

datafile = "2013_ERCOT_Hourly_Load_Data.xls"
outfile = "2013_Max_Loads.csv"


def open_zip(datafile):
    with ZipFile('{0}.zip'.format(datafile), 'r') as myzip:
        myzip.extractall()


def parse_file(datafile):
    workbook = xlrd.open_workbook(datafile)
    sheet = workbook.sheet_by_index(0)
    data = []
    fieldnames = ['Station', 'Max Load', 'Year', 'Month', 'Day', 'Hour']
    # YOUR CODE HERE
    # Remember that you can use xlrd.xldate_as_tuple(sometime, 0) to convert
    # Excel date to Python tuple of (year, month, day, hour, minute, second)
    data.append(fieldnames)
    for i in range(1, 9):
        region_header = sheet.cell_value(0, i)
        region_data = sheet.col_values(i, start_rowx=1, end_rowx=None)
        region_max = max(region_data)
        region_max_index = sheet.col_values(i).index(region_max)
        region_max_date_xls = sheet.cell_value(region_max_index, 0)
        region_max_date = xlrd.xldate_as_tuple(region_max_date_xls, 0)
        data.append({'Station': region_header,
                     'Max Load': region_max,
                     'Year': region_max_date[0],
                     'Month': region_max_date[1],
                     'Day': region_max_date[2],
                     'Hour': region_max_date[3]})
    return data


def save_file(data, filename):
    csvfile = open(filename, 'wb')
    fieldnames = data.pop(0)
    wr = csv.DictWriter(csvfile, delimiter="|", fieldnames=fieldnames)
    wr.writerow(dict((fn, fn) for fn in fieldnames))
    for row in data:
        wr.writerow(row)


def test():
    open_zip(datafile)
    data = parse_file(datafile)
    save_file(data, outfile)

    number_of_rows = 0
    stations = []

    ans = {'FAR_WEST': {'Max Load': '2281.2722140000024',
                        'Year': '2013',
                        'Month': '6',
                        'Day': '26',
                        'Hour': '17'}}
    correct_stations = ['COAST', 'EAST', 'FAR_WEST', 'NORTH',
                        'NORTH_C', 'SOUTHERN', 'SOUTH_C', 'WEST']
    fields = ['Year', 'Month', 'Day', 'Hour', 'Max Load']

    with open(outfile) as of:
        csvfile = csv.DictReader(of, delimiter="|")
        for line in csvfile:
            station = line['Station']
            if station == 'FAR_WEST':
                for field in fields:
                    # Check if 'Max Load' is within .1 of answer
                    if field == 'Max Load':
                        max_answer = round(float(ans[station][field]), 1)
                        max_line = round(float(line[field]), 1)
                        assert max_answer == max_line

                    # Otherwise check for equality
                    else:
                        assert ans[station][field] == line[field]

            number_of_rows += 1
            stations.append(station)

        # Output should be 8 lines not including header
        assert number_of_rows == 8

        # Check Station Names
        assert set(stations) == set(correct_stations)


if __name__ == "__main__":
    test()
