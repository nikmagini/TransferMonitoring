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
field_delimter = "|"  # to seperate flatened fields
cvs_field_ph = -1    # placeholder for empty atribute
cvs_field_sph = -2    # placeeholder for blanklines
cvs_field_nph = -3    # placeeholder for null
# list of fields that I should put first in CSV file
important_fields = ['tr_id', 'timestamp_tr_st',
                    'timestamp_tr_comp', 'timestamp_tr_dlt']


def representsInt(s):
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


def reorderKeyList(key_list, import_k_l):
    """put important keys in front of list"""
    for key in import_k_l:
        try:
            key_list.remove(key)
            key_list.append(key)
        except Exception:
            print("There wasn't such key: " + key)
    return key_list


def readFolderToList(FolderPath):
    """Function takes path to folder, then"""
    records_list = []
    for root, directories, filenames in os.walk(FolderPath):
        for filename in filenames:
            if filename.endswith(".json"):
                a = os.path.join(root, filename)
                records_list += readFileToList(a)
            else:
                continue
    return records_list


def readFileToList(filename):
    """Function takes path of file,
    read records one by one and puts it Json objects to list """

    # create list of special control charracters
    escapes = ''.join([chr(char) for char in range(1, 32)])
    with open(filename) as json_file:
        rec_list = []
        if debug is True:
            print("-----------")
        for line in json_file:
            json_dict = flatten_dict(json.loads(line.translate(None, escapes)))
            rec_list.append(json_dict)
    if debug is True:
        print rec_list[0]
        print "-------------"
        print rec_list[5]
    return rec_list


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
                if(representsInt(value)):
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
    inputfile = os.path.join(working_path, "data/smallJsonData.json")
    inputdir = os.path.join(working_path, "data/testFolder")
    outputfile = '/tmp/JsonToCsvDefault'
    # flag that says if user wants to scan folder instead of 1 file
    its_a_dir = False

    try:
        opts, args = getopt.getopt(
            argv, "hi:o:d", ["ifile=", "ofile=", "dir="])
    except getopt.GetoptError:
        print 'test.py -i <inputfile> -o <outputfile>'
        sys.exit(2)
    for opt, arg in opts:
        if opt == '-h':
            print 'test.py -i <inputfile> -o <outputfile>'
            print 'test.py --dir <inputdir> -o <outputfile>'
            print "default parameters are taken if arguments are not specified:"
            print "<inputfile>: " + inputfile
            print "<inputdir>: " + inputdir
            print "<outputfile>: " + outputfile + '_org.csv'
            print "<outputfile>: " + outputfile + '_hash.csv'
            sys.exit()
        elif opt in ("-i", "--ifile"):
            inputfile = arg
        elif opt in ("-o", "--ofile"):
            outputfile = arg
        elif opt in ("-d"):
            global debug
            debug = True
        elif opt in ("--dir"):
            its_a_dir = True
            inputdir = arg

    if debug is True:
        print("-----------")
        print 'Input file is "', inputfile
        print 'Output file is "', outputfile
        print("-----------")

    # check if input file exists
    # if (os.path.isfile(inputfile) is True):
    #     pass
    # else:
    #     print("the input file specified does not exist:\n" + inputfile)
    #     sys.exit(2)
    # ---------------------------------

    # if it is a folder, itarate trough folder, give each file to the
    # function and concetinate results
    try:
        if its_a_dir is True:
            records_list = readFolderToList(inputdir)
        else:
            records_list = readFileToList(inputfile)
    except Exception, e:
        print("Something went wrong:")
        print e
        raise
        sys.exit(2)

    records_list = addDeltaTimeField(records_list)

    # take all unique keys from list and put to set and order it
    records_keys = set()
    for item in records_list:
        a = item.keys()
        records_keys = records_keys.union(set(a))
    records_keys = sorted(records_keys)

    if debug is True:
        print records_keys

    records_keys = reorderKeyList(records_keys, important_fields)
    # write haseverything to CSV file
    jsonListToCSV(records_list, records_keys, outputfile + '_org.csv')

    # write haseverything to CSV file with hashed values
    records_list = recordsListTransform(records_list)
    if debug is True:
        for key, value in records_list[8].items():
            print key, value, type(value)
    jsonListToCSV(records_list, records_keys, outputfile + '_hash.csv')


if __name__ == '__main__':
    main(sys.argv[1:])

    # TODO: use log file instead of print (tmp/filename-date.txt(?))
    # TODO: put all variable declaration at the begining of script
