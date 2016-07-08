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
debug = True        # to output debug info
field_delimter = "|"  # to seperate flatened fields
cvs_field_ph = -1    # placeholder for empty atribute
cvs_field_sph = -2    # placeeholder for blanklines
cvs_field_nph = -3    # placeeholder for null

def RepresentsInt(s):
    """check if string can be typecasted to int"""
    try:
        int(s)
        return True
    except ValueError:
        return False

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


def readFolderToList(FolderPath):
    """Function takes path to folder, then"""
    # TODO: for each filename call readFileToList() and concotinate them
    # TODO: implement


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
        if debug is True:
            print("-----------")
        for line in json_file:
            json_dict = flatten_dict(json.loads(line.translate(None, escapes)))
            list.append(json_dict)
            # a += 1
    if debug is True:
        print list[0]
        print "-------------"
        print list[5]
    return list


def stringToHash(string):
    """it will take atribute, probably string and return a big integer"""
    return int(hashlib.md5(string).hexdigest(), 16)


def recordsListTransform(records_list):
    """Function will take list of dictonaries and transfor
    its artibutes.
    If it is a string, transform it to either primary type [int|boolean|etc]
    or to hash number"""
    for record in records_list:
        for key, value in record.items():
            if isinstance(value, basestring):
                if(RepresentsInt(value)):
                    record[key] = int(value)
                elif(value.upper() == 'TRUE'):
                    record[key] = True
                elif(value.upper() == 'FALSE'):
                    record[key] = False
                elif(value == ""):
                    record[key] = cvs_field_sph
                else:
                    record[key] = stringToHash(value)
            elif(value is None):
                record[key] = cvs_field_nph

    return records_list


def jsonListToCSV(jsonList, keysSet, outputPath):
    """Function that proceses list and output results to Csv file"""
    outputhFile = open(outputPath, 'w')
    csvwriter = csv.DictWriter(
        outputhFile, fieldnames=keysSet, restval=cvs_field_ph)
    csvwriter.writeheader()
    for record_dict in jsonList:
        csvwriter.writerow(record_dict)
    outputhFile.close()
    return 0


def addDeltaTimeField(jsonList):
    """take list if json dictonaries add to each add atributes"""
    for record_dict in jsonList:
        try:
            record_dict['timestamp_tr_dlt'] = \
                int(record_dict['timestamp_tr_comp'])\
                - int(record_dict['timestamp_tr_st'])
        except Exception, e:
            if debug is True:
                print("Something was wrong: ", e)
        else:
            pass

    return jsonList


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
    if debug is True:
        print("-----------")
        print 'Input file is "', inputfile
        print 'Output file is "', outputfile
        print("-----------")

    # check if input file exists
    if (os.path.isfile(inputfile) is True):
        pass
    else:
        print("the input file specified does not exist:\n" + inputfile)
        sys.exit(2)

    # ---------------------------------

    # TODO: if it is a folder, itarate trough folder, give each file to the
    # function and concetinate results
    records_list = readFileToList(inputfile)
    records_list = addDeltaTimeField(records_list)
    # take all unique keys from list and put to set and order it
    records_keys = set()
    for item in records_list:
        a = item.keys()
        records_keys = records_keys.union(set(a))
    records_keys = sorted(records_keys)

    if debug is True:
        print records_keys

    records_list = recordsListTransform(records_list)
    # if debug == True:
        # for key, value in records_list[8].items():
        #     print key, value, type(value)

    # write everything to CSV file
    jsonListToCSV(records_list, records_keys, outputfile)


if __name__ == '__main__':
    main(sys.argv[1:])

    # TODO: delete all unecesary commented lines
    # TODO: add delta field
    # TODO: add option to iterate trough fields
    # TODO: delet unecsary files
    # TODO: rearange intresting fields position
    # TODO: save 2 seperate csv files (before and after hash function)
    # TODO: use log file instead of print (tmp/filename-date.txt(?))
    # TODO: put all variable declaration at the begining of script
