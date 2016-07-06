"""
File       : jsonUtilities.py
Author     : Zygimantas Matonis
Description: Script to convert Json records to CSV
"""

import json
import csv
import os
import sys
import getopt  # http://www.tutorialspoint.com/python/python_command_line_arguments.htm
import hashlib

# global variables
debug = False        # to output debug info
field_delimter = "|"  # to seperate slatened fields
cvs_field_ph = -1    # placeholder for empty atribute


def flatten_dict(d):
    """takes dict object and flatens it using dot notation"""
    def items():
        for key, value in d.items():
            if isinstance(value, dict):
                for subkey, subvalue in flatten_dict(value).items():
                    yield key + field_delimter + subkey, subvalue
            else:
                yield key, value

    return dict(items())


def readFileToList(filename):
    """Function takes path of file,
    read records one by one and puts it Json objects to list """

    # create list of special control charracters
    escapes = ''.join([chr(char) for char in range(1, 32)])
    with open(filename) as json_file:
        # employee_parsed = json.load(json_file)
        # list = json_file.readline
        # print json_file.readline
        # -----------
        # a = 0
        list = []
        if debug == True:
            print("-----------")
        for line in json_file:
            json_dict = flatten_dict(json.loads(line.translate(None, escapes)))
            list.append(json_dict)
            # a += 1
    if debug == True:
        print list[0]
        print "-------------"
        print list[5]
    return list


def stringToHash(string):
    """it will take atribute, probably string and return a big integer"""
    return int(hashlib.md5(string).hexdigest(), 16)


def recordsListTransform(records_list, records_keys):
    """Function will take list of dictonaries and transfor
    its artibutes.
    If it is a string, transform it to either primary type [int|boolean|etc]
    or to hash number"""

    def RepresentsInt(s):
        try:
            int(s)
            return True
        except ValueError:
            return False
            # TODO: finish and check code
    for record in records_list:
        for key, value in record:
            if isinstance(value, basestring):
                if(RepresentsInt(value)):
                    record[key] = int(value)
                elif(value.upper() == 'TRUE'):
                    record[key] = True
                elif(value.upper() == 'False'):
                    record[key] = False

    return 1


def JsonListToCSV(jsonList, keysSet, outputPath):
    """ that procesed list and output to cvs """
    # TODO: implement
    outputhFile = open(outputPath, 'w')
    csvwriter = csv.DictWriter(
        outputhFile, fieldnames=keysSet, restval=cvs_field_ph)
    csvwriter.writeheader()
    for record_dict in jsonList:
        # print keysSet
        # if count == 0:
        #     header = list(keysSet)
        #     csvwriter.writerow(header)
        #     count += 1
        csvwriter.writerow(record_dict)
    outputhFile.close()
    return 0


def main(argv):
    """Main function"""

    working_path = os.path.dirname(os.path.abspath(__file__))
    # inpath = os.path.join(working_path, "data/smallJsonData.json")
    # print path

    inputfile = os.path.join(working_path, "data/smallJsonData.json")
    outputfile = '/tmp/JsonToCsvDefault.csv'
    try:
        opts, args = getopt.getopt(argv, "hi:o:d", ["ifile=", "ofile="])
    except getopt.GetoptError:
        print 'test.py -i <inputfile> -o <outputfile>'
        sys.exit(2)
    for opt, arg in opts:
        if opt == '-h':
            print 'test.py -i <inputfile> -o <outputfile>'
            print "default parameters are taken if arguments are not specified:"
            print "<inputfile>: " + inputfile
            print "<outputfile>: " + outputfile
            sys.exit()
        elif opt in ("-i", "--ifile"):
            inputfile = arg
        elif opt in ("-o", "--ofile"):
            outputfile = arg
        elif opt in ("-d"):
            global debug
            debug = True
    if debug == True:
        print("-----------")
        print 'Input file is "', inputfile
        print 'Output file is "', outputfile
        print("-----------")

    # check if input file exists
    if (os.path.isfile(inputfile) == True):
        pass
    else:
        print("the input file specified does not exist:\n" + inputfile)
        sys.exit(2)

    # ---------------------------------

    # TODO: when writing files back, check atribute if its a string - if yes,
    # cast to number with hash function

    # TODO: if it is a folder, itarate trough folder, give each file to the
    # function and concetinate results
    records_list = readFileToList(inputfile)

    # take all unique keys from list and put to set and order it
    records_keys = set()
    for item in records_list:
        a = item.keys()
        records_keys = records_keys.union(set(a))
    records_keys = sorted(records_keys)

    if debug == True:
        print keys

    for key, value in records_list[0].items():
        print key, value, type(value)

    # JsonListToCSV(records_list,records_keys,outputfile)

if __name__ == '__main__':
    main(sys.argv[1:])
