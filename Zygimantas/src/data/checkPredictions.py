"""
File       : jsonUtilities.py
Author     : Zygimantas Matonis
Description: Script to check predicted data with actual values
             and calculate ..
"""
# TODO: finish docs

import json
import csv
import os
import sys
import getopt  # http://www.tutorialspoint.com/python/python_command_line_arguments.htm
import itertools


def main(argv):
    """Main function"""
    # todo implement random split of dataset
    predictFile = '/tmp/pred.txt'
    realFiles = '/tmp/test.csv'
    resultsFile = '/tmp/results.txt'

    label = 'timestamp_tr_dlt'

    # TODO: implet option input
    # try:
    #     opts, args = getopt.getopt(
    #         argv, "hi:o:d", ["ifile=", "ofile=", "dir="])
    # except getopt.GetoptError:
    #     print 'checkPredictions.py -p <inputfile> - <outputfile>'
    #     sys.exit(2)
    # for opt, arg in opts:
    #     if opt == '-h':
    #         print 'checkPredictions.py -i <inputfile> -o <outputfile>'
    #         sys.exit(2)
    #     elif opt in ("-i", "--ifile"):
    #         inputfile = arg
    #     elif opt in ("-o", "--ofile"):
    #         outputfile = arg

    try:
        with open(predictFile, 'r') as predicted_val, \
                open(realFiles, 'r') as real_val, \
                open(resultsFile, 'w') as results_wr:
            real_Readercsv = csv.DictReader(real_val)
            # for a in real_Readercsv:
            #     print a

            predicted_val.readline()
            header = "Real_value, Predict, absolute_diference\n"
            results_wr.write(header)
            count = 0
            total_offset = 0
            for f, b in itertools.izip(real_Readercsv, predicted_val):
            # TODO: try to catch -1
                String = "{0}, {1}, {2}\n".format(
                    f[label], b.rstrip(), + abs(float(f[label]) - float(b)))
                results_wr.write(String)
                count += 1
                total_offset += abs(float(f[label]) - float(b))
            MSE = total_offset / count
            String = "----------------\n"
            String += "MAE: {0}".format(MSE)
            results_wr.write(String)
    except Exception, e:
        raise


if __name__ == '__main__':
    main(sys.argv[1:])
