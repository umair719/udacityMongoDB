__author__ = 'Umair'
#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Let's assume that you combined the code from the previous 2 exercises
# with code from the lesson on how to build requests, and downloaded all the data locally.
# The files are in a directory "data", named after the carrier and airport:
# "{}-{}.html".format(carrier, airport), for example "FL-ATL.html".
# The table with flight info has a table class="dataTDRight".
# There are couple of helper functions to deal with the data files.
# Please do not change them for grading purposes.
# All your changes should be in the 'process_file' function
# This is example of the datastructure you should return
# Each item in the list should be a dictionary containing all the relevant data
# Note - year, month, and the flight data should be integers
# You should skip the rows that contain the TOTAL data for a year
# data = [{"courier": "FL",
# "airport": "ATL",
# "year": 2012,
# "month": 12,
# "flights": {"domestic": 100,
# "international": 100}
#         },
#         {"courier": "..."}
# ]
from zipfile import ZipFile
import os

from bs4 import BeautifulSoup


datadir = "data"


def open_zip(datadir):
    with ZipFile('{0}.zip'.format(datadir), 'r') as myzip:
        myzip.extractall()


def process_all(datadir):
    files = os.listdir(datadir)
    return files


def process_file(f):
    """This is example of the data structure you should return.
    Each item in the list should be a dictionary containing all the relevant data
    from each row in each file. Note - year, month, and the flight data should be
    integers. You should skip the rows that contain the TOTAL data for a year
    data = [{"courier": "FL",
            "airport": "ATL",
            "year": 2012,
            "month": 12,
            "flights": {"domestic": 100,
                        "international": 100}
            },
            {"courier": "..."}
    ]
    """
    data = []
    info = {}
    info["courier"], info["airport"] = f[:6].split("-")

    with open("{}/{}".format(datadir, f), "r") as html:
        soup = BeautifulSoup(html)
        for row in soup.findAll('tr', attrs={'class': 'dataTDRight'}):
            if not row.findAll(text='TOTAL'):
                td = row.find_all('td')
                d = {"courier": "FL",
                     "airport": "ATL",
                     "year": int(td[0].string),
                     "month": int(td[1].string),
                     "flights": {"domestic": int(td[2].string.replace(',', '')),
                                 "international": int(td[3].string.replace(',', ''))}
                }
                data.append(d)
    return data


def test():
    print
    "Running a simple test..."
    # open_zip(datadir)
    files = process_all(datadir)
    data = []
    for f in files:
        data += process_file(f)
    assert len(data) == 399  # Total number of rows
    for entry in data[:3]:
        assert type(entry["year"]) == int
        assert type(entry["month"]) == int
        assert type(entry["flights"]["domestic"]) == int
        assert len(entry["airport"]) == 3
        assert len(entry["courier"]) == 2
    assert data[-1]["airport"] == "ATL"
    assert data[-1]["flights"] == {'international': 108289, 'domestic': 701425}

    print
    "... success!"


if __name__ == "__main__":
    test()