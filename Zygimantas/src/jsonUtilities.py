"""
File       : jsonUtilities.py
Author     : Zygimantas Matonis
Description: Helper functions to extract records from json document
"""

import json
import csv
import os
import sys
import getopt  # http://www.tutorialspoint.com/python/python_command_line_arguments.htm
import hashlib

# global variable which if true outputs debug data
debug = False


def flatten_dict(d):
    """takes dict object and flatens it using dot notation"""
    def items():
        for key, value in d.items():
            if isinstance(value, dict):
                for subkey, subvalue in flatten_dict(value).items():
                    yield key + "." + subkey, subvalue
            else:
                yield key, value

    return dict(items())


def readFileToList(filename):
    escapes = ''.join([chr(char) for char in range(1, 32)])

    """Function takes path of file,
    read records one by one and puts it Json objects to list """
    # Hint: maybe I could write it as a generator using yield
    with open(filename) as json_file:
        # employee_parsed = json.load(json_file)
        # list = json_file.readline
        # print json_file.readline
        # -----------
        # create list of special control charracters
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

# unnecessary function

# def flatenJsonObject(json_object):
#     """Function that will take json object record and flaten nested atibutes
#     to example transfer.start, transfer.end and etc. """
#     # TODO: implement
#     return list


def stringToHash(string):
    """it will take atribute, probably string and return integer"""
    return int(hashlib.sha224(string).hexdigest(), 16)


def JsonListToCSV(jsonList):
    """ that procesed list and output to cvs """
    # TODO: implement
    return


def main(argv):
    "Main function"
    # TODO: give paths to input output files/folder as argument
    # TODO: give path to output path as well with default values
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
    # print 'Input file is "', inputfile
    # print 'Output file is "', outputfile

    # print os.path.isfile(inputfile)
    if (os.path.isfile(inputfile) == True):
        pass
    else:
        print("the input file specified does not exist:\n" + inputfile)
        sys.exit(2)
    list = readFileToList(inputfile)


if __name__ == '__main__':
    main(sys.argv[1:])
