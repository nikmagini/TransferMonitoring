"""
File       : jsonUtilities.py
Author     : Zygimantas Matonis
Description: Helper functions to extract records from json document
"""

import json
import csv
import os

def readFileToList(filename):
    """Function takes path of file,
    read records one by one and puts it Json objects to list """
    # TODO: implement it
    # Hint: maybe I could write it as a generator using yield
    return list

def flatenJsonObject(json_object):
    """Function that will take json object record and flaten nested atibutes to
    example transfer.start, transfer.end and etc. """
    # TODO: implement
    return list

def stringToHash(atribute):
    """it will take atribute, probably string and return integer"""
    #TODO: implement
    return smt

def main():
    "Main function"

    ## the ugly way to run on test data
    # os.path.dirname(os.path.abspath(__file__))
    working_path= os.path.dirname(os.path.abspath(__file__))
    path = os.path.join(working_path,"data/recordsExample.json")
    print path
    # file_path
    # TODO: for startes list nice list

if __name__ == '__main__':
    main()
