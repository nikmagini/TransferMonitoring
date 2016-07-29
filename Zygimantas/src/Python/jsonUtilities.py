#!/usr/bin/env python
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
import logging
import inspect
import types

# global variables
debug = False        # to output debug info
field_delimter = "|"  # to seperate flatened fields
cvs_field_ph = -1    # placeholder for empty atribute
cvs_field_sph = -2    # placeeholder for blanklines
cvs_field_nph = -3    # placeeholder for null
# list of fields that I should put first in CSV file
important_fields = ['tr_id', 'timestamp_tr_st',
                    'timestamp_tr_comp', 'timestamp_tr_dlt']

# logger and logger config

logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

# files
working_path = os.path.dirname(os.path.abspath(__file__))
inputfile = os.path.join(working_path, "../../data/testFolder")
# inputfile = os.path.join(working_path, "../../data/smallJsonData.json")
outputfile = '/tmp/JsonToCsvDefault'


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


def readFolderToListGenerator(FolderPath):
    """Function takes path to folder, then"""
    for root, directories, filenames in os.walk(FolderPath):
        for filename in filenames:
            if filename.endswith(".json"):
                a = os.path.join(root, filename)
                yield readFileToListGenerator(a)


def readFileToListGenerator(filename):
    """Function takes path of file,
    read records one by one and puts it Json objects to list """
    logger.info('Reading file to list: '+ filename)
    # create list of special control charracters
    escapes = ''.join([chr(char) for char in range(1, 32)])
    with open(filename) as json_file:
        for line in json_file:
            json_dict = flatten_dict(json.loads(line.translate(None, escapes)))
            logger.debug(json_dict)
            yield json_dict


def stringToHash(string):
    """it will take atribute, probably string and return a big integer"""
    return int(hashlib.md5(string).hexdigest()[:30], 16)

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
                    record[key] = 1
                elif(value.upper() == 'FALSE'):
                    record[key] = 0
                elif(value == ""):
                    record[key] = cvs_field_sph
                else:
                    record[key] = stringToHash(value)
            elif(value is None):
                record[key] = cvs_field_nph
            elif(value is True):
                record[key] = 1
            elif(value is False):
                record[key] = 0

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

# TODO: will not work with yield aproach
def addDeltaTimeField(jsonList):
    """take list if json dictonaries add to each add atributes"""
    for record_dict in jsonList:
        try:
            record_dict['timestamp_tr_dlt'] = \
                int(record_dict['timestamp_tr_comp'])\
                - int(record_dict['timestamp_tr_st'])
        except Exception as e:
            logger.exception("Fields mising: ", e)

    return jsonList

def keys_from_gen(gen_function):
    key_set = set()
    for item in gen_function:
        a = None
        if isinstance(item, types.GeneratorType):
            a = keys_from_gen(item)
        else:
            a = item.keys()
        key_set = key_set.union(set(a))
    return key_set


def main(argv):
    """Main function"""

    # flag that says if user wants to scan folder instead of 1 file
    # its_a_dir = False
    global inputfile, outputfile, working_path

    try:
        opts, args = getopt.getopt(
            argv, "hi:o:d", ["ifile=", "ofile=", "dir="])
    except getopt.GetoptError:
        print 'jsonUtilities.py -i <inputfile> -o <outputfile>'
        print 'jsonUtilities.py --dir <inputdir> -o <outputfile>'
        print "default parameters are taken if arguments are not specified:"
        print "<inputfile>: " + inputfile
        print "<outputfile>: " + outputfile + '_org.csv'
        print "<outputfile>: " + outputfile + '_hash.csv'
        sys.exit(2)
    for opt, arg in opts:
        if opt == '-h':
            print 'jsonUtilities.py -i <inputfile> -o <outputfile>'
            print 'jsonUtilities.py --dir <inputdir> -o <outputfile>'
            print "default parameters are taken if arguments are not specified:"
            print "<inputfile>: " + inputfile
            print "<outputfile>: " + outputfile + '_org.csv'
            print "<outputfile>: " + outputfile + '_hash.csv'
            sys.exit(2)
        elif opt in ("-i", "--ifile"):
            inputfile = arg
        elif opt in ("-o", "--ofile"):
            outputfile = arg
        # elif opt in ("-d"):
        #     global debug
        #     debug = True
        # elif opt in ("--dir"):
        #     its_a_dir = True
        #     inputdir = arg

    # check if input is file or directory

    try:
        if os.path.isdir(inputfile):
            logger.info('Input dir is: '+ inputfile)
            records_list_generator = readFolderToListGenerator
        elif os.path.isfile(inputfile):
            records_list_generator = readFileToListGenerator
            logger.info('Input file is: '+ inputfile)
        else:
            logger.warning('Input direction/file '
                             'does not exist:' + inputfile)
            sys.exit(2)
    except Exception as e:
        logger.exception(e)
        sys.exit(2)

    logger.info('Output file is: '+ outputfile)

    # TODO: should add on the fly, not to seperate list
    # recordsListGenerator = addDeltaTimeField(recordsListGenerator)

    # take all unique keys from list and put to set and order it
    records_keys = keys_from_gen(records_list_generator(inputfile))

    # sort list keys alphabetically
    records_keys = sorted(records_keys)
    logger.debug('Sorted key list :')
    logger.debug(records_keys)

    # for item in recordsListGenerator:
    # recordsListGenerator = recordsListGenerator(inputfile)
    # print "--------"
    # for item in recordsListGenerator:
    #     print item

    records_keys = reorderKeyList(records_keys, important_fields)

    # write every thing to CSV file
    jsonListToCSV(records_list_generator, records_keys, outputfile + '_org.csv')

    # write haseverything to CSV file with hashed values
    records_list_generator = recordsListTransform(records_list_generator)

    # if debug is True:
    #     for key, value in recordsListGenerator[8].items():
    #         print key, value, type(value)

    jsonListToCSV(records_list_generator, records_keys, outputfile + '_hash.csv')


if __name__ == '__main__':
    main(sys.argv[1:])

    # TODO: use log file instead of print (tmp/filename-date.txt(?))
    # TODO: put all variable declaration at the begining of script
