__author__ = 'Umair'

"""
Your task is to check the "productionStartYear" of the DBPedia autos datafile for valid values.
The following things should be done:
-[X] check if the field "productionStartYear" contains a year
-[X] check if the year is in range 1886-2014
-[X] convert the value of the field to be just a year (not full datetime)
-[X] the rest of the fields and values should stay the same
-[X] if the value of the field is a valid year in range, as described above,
  write that line to the output_good file
-[X] if the value of the field is not a valid year,
  write that line to the output_bad file
-[X] discard rows (neither write to good nor bad) if the URI is not from dbpedia.org
-[X] you should use the provided way of reading and writing data (DictReader and DictWriter)
  They will take care of dealing with the header.

You can write helper functions for checking the data and writing the files, but we will call only the
'process_file' with 3 arguments (inputfile, output_good, output_bad).
"""
import csv
import re

INPUT_FILE = 'autos1.csv'
OUTPUT_GOOD = 'autos-valid.csv'
OUTPUT_BAD = 'FIXME-autos.csv'


def process_file(input_file, output_good, output_bad):
    with open(input_file, "r") as f:
        reader = csv.DictReader(f)
        header = reader.fieldnames
        gdata = []
        bdata = []
        # COMPLETE THIS FUNCTION
        for row in reader:
            if re.search("dbpedia.org", row['URI']):
                if re.match('^(188[6-9]|189[0-9]|19[0-9][0-9]|200[0-9]|201[0-4])', row['productionStartYear']):
                    row['productionStartYear'] = row['productionStartYear'][0:4]
                    gdata.append(row)
                else:
                    bdata.append(row)

    with open(output_good, "w") as g:
        gwriter = csv.DictWriter(g, delimiter=",", lineterminator='\n', fieldnames=header)
        gwriter.writeheader()
        for row in gdata:
            gwriter.writerow(row)

    with open(output_bad, "w") as g:
        bwriter = csv.DictWriter(g, delimiter=",", lineterminator='\n', fieldnames=header)
        bwriter.writeheader()
        for row in bdata:
            bwriter.writerow(row)


def test():
    process_file(INPUT_FILE, OUTPUT_GOOD, OUTPUT_BAD)


if __name__ == "__main__":
    test()
