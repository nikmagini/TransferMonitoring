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
field_delimter = "|"  # to seperate flatened fields
cvs_field_ph = -1    # placeholder for empty atribute
cvs_field_sph = -2    # placeeholder for blanklines
cvs_field_nph = -3    # placeeholder for null
# list of fields that I should put first in CSV file
important_fields = ['tr_id', 'timestamp_tr_st',
                    'timestamp_tr_comp', 'timestamp_tr_dlt']
new_fields =['timestamp_tr_dlt']

# logger and logger config
# https://docs.python.org/2/library/logging.html
FORMAT = '%(levelname)s - %(funcName)s - %(lineno)d: %(message)s'
logging.basicConfig(level=logging.INFO, format=FORMAT)
logger = logging.getLogger(__name__)

# files:
working_path = os.path.dirname(os.path.abspath(__file__))

# inputfile = os.path.join(working_path, "../../data/testFolder")
# inputfile = os.path.join(working_path, "../../data/smallJsonData.json")
inputfile = None

outputfile_org = '/tmp/JsonToCsvDefault_org.csv'
outputfile_org = None

# outputfile_hash = '/tmp/JsonToCsvDefault_hash.csv'
outputfile_hash = None


def representsInt(s):
    """check if string can be typecasted to int"""
    try:
        int(s)
        return True
    except ValueError:
        return False


def flatten_dict(d):
    """takes dict object and flatens it using delimeter """
    def items():
        for key, value in d.items():
            if isinstance(value, dict):
                for subkey, subvalue in flatten_dict(value).items():
                    yield key + field_delimter + subkey, subvalue
            else:
                yield key, value

    return dict(items())


def reorderKeyList(key_list, import_k_l,new_fields):
    """put important keys in front of list"""

    # and new fields to list
    key_list = key_list + new_fields

    # reoder keys
    for key in import_k_l:
        try:
            key_list.remove(key)
            key_list.append(key)
        except Exception:
            print("There wasn't such key: " + key)
    return key_list


def readFolderToListGenerator(FolderPath):
    """
    Function takes path to folder, then
    calls readFileToListGenerator() and yields
    dict type object
    """
    for root, directories, filenames in os.walk(FolderPath):
        for filename in filenames:
            if filename.endswith(".json"):
                a = os.path.join(root, filename)
                for json_dict in readFileToListGenerator(a):
                    yield json_dict

def readFileToListGenerator(filename):
    """
    :param filename: path to file
    :return json_dict: dict{} type object

    Function takes path of file,
    read records one by one and yields
    dict type object with json record data already flatened
    """

    logger.info('Reading file: %s', filename)
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


def recordsListTransform(records_dict):
    """
    Function will dictonary and transfor its artibutes.
    If it is a string, transform it to either primary type [int|boolean|etc]
    or to hash number
    """

    for key, value in records_dict.items():
        if isinstance(value, basestring):
            if(representsInt(value)):
                records_dict[key] = int(value)
            elif(value.upper() == 'TRUE'):
                records_dict[key] = 1
            elif(value.upper() == 'FALSE'):
                records_dict[key] = 0
            elif(value == ""):
                records_dict[key] = cvs_field_sph
            else:
                records_dict[key] = stringToHash(value)
        elif(value is None):
            records_dict[key] = cvs_field_nph
        elif(value is True):
            records_dict[key] = 1
        elif(value is False):
            records_dict[key] = 0
    return records_dict


def jsonListToCSV(jsonList, keysSet, outputPath, hash_f=False ):
    """
    Function that processes list and output results to Csv file
    """

    outputhFile = open(outputPath, 'w')
    csvwriter = csv.DictWriter(
        outputhFile, fieldnames=keysSet, restval=cvs_field_ph)
    csvwriter.writeheader()
    logger.debug('File writing')
    for record_dict in jsonList:
        record_dict = addDeltaTimeField(record_dict)
        if hash_f is True: # to hash values
            record_dict = recordsListTransform(record_dict)

        logger.debug(record_dict)
        csvwriter.writerow(record_dict)
    outputhFile.close()
    return 0

def addDeltaTimeField(jsonDict):
    """
    :param jsonDict : dict{}
    :return josnDict : dict{}
    take dict{} object and add new atribute 'timestamp_tr_dlt'
    """
    try:
        jsonDict['timestamp_tr_dlt'] = \
            int(jsonDict['timestamp_tr_comp'])\
            - int(jsonDict['timestamp_tr_st'])
    except Exception as e:
        # in case timestamp_tr_comp and timestamp_tr_st
        # are empty
        logger.debug(e)
        jsonDict['timestamp_tr_dlt'] = cvs_field_ph
    return jsonDict

def keys_from_gen(gen_function):
    '''
    :param gen_function: takes generator and extracts unique dictonary field names
    :return: set()
    '''
    '''
    :param gen_function:
    :return:
    '''
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
    global inputfile,  outputfile_org, outputfile_hash, working_path

    message= 'Convertes .json file/folder with .json to .csv\n' \
             'To run :\n' \
             'jsonUtilities.py --ifile <inputfile.json|dir> --ofile <outputfile.csv> \n\n' \
             '--ohfile <output_hashedfile.csv> --log <LEVEL>\n\n' \
             'example: \n' \
             'jsonUtilities.py --ifile ../../data/testFolder --ohfile ' \
             '/tmp/output_hashed.csv --log WARNING \n'\
             '-h : shows this help \n' \
             '-i/--ifile : input file or a directory \n' \
             '-o/--ofile : path/to/extracted/output.csv \n'\
             '--ohfile : path/to/hashed/output.csv \n' \
             '--log : message level [DEBUG|INFO|WARNING|ERROR|CRITICAL] \n'

    try:
        opts, args = getopt.getopt(
            argv, "hi:o:", ["ifile=", "ofile=", "ohfile=","log="])
    except getopt.GetoptError:
        print('ERROR:Wrong arguments'
              'run \'jsonUtilities.py -h\' for more info')
        sys.exit(2)

    for opt, arg in opts:
        if opt == '-h':
            print(message)
            sys.exit(2)
        elif opt in ("-i", "--ifile"):
            inputfile = arg
        elif opt in ("-o", "--ofile"):
            outputfile_org = arg
        elif opt == "--ohfile":
            outputfile_hash = arg
        elif opt == '--log':
            try:
                logger.setLevel(arg.upper())
            except Exception as e:
                logger.warning('%s, using INFO logging level ',e)

    if not (inputfile and (outputfile_hash or outputfile_org)):
        print('Atleast input and one output parameter should be given, '
              'run \'jsonUtilities.py -h\' for more info')
        sys.exit(2)


    # end of user input
    # ---------------
    # check if input is file or directory
    try:
        if os.path.isdir(inputfile):
            logger.info('Input directory is: %s', inputfile)
            records_list_generator = readFolderToListGenerator
        elif os.path.isfile(inputfile):
            records_list_generator = readFileToListGenerator
            logger.info('Input file is: %s', inputfile)
        else:
            logger.warning('Input direction/file '
                             'does not exist: %s', inputfile)
            sys.exit(2)
    except Exception as e:
        logger.exception(e)
        sys.exit(2)
    logger.info('Output file file with original values: %s', outputfile_org)
    logger.info('Output file with hashed values: %s', outputfile_hash)
    # end of file checking
    # ---------------

    # take all unique keys from list and put to set and order it
    records_keys = keys_from_gen(records_list_generator(inputfile))

    # sort list keys alphabetically
    records_keys = sorted(records_keys)

    # add new fiels and change few fields position
    records_keys = reorderKeyList(records_keys, important_fields,new_fields)
    logger.debug('Sorted key list : %s', records_keys)

    # write every thing to CSV file
    if outputfile_org:
        jsonListToCSV(records_list_generator(inputfile), records_keys, outputfile_org, hash_f=False)

    # write every thing to CSV file with Hashed values
    if outputfile_hash:
        jsonListToCSV(records_list_generator(inputfile), records_keys, outputfile_hash, hash_f=True )


if __name__ == '__main__':
    main(sys.argv[1:])
