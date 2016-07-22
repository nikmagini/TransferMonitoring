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
import numpy


def main(argv):
    """Main function"""
    # todo implement random split of dataset
    predictFile = '/tmp/predic.txt'
    realFiles = '/tmp/test.csv'
    resultsFile = '/tmp/check_results.txt'

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
            header = "Real_value,Predict,Absolute_diference"
            header += ",Diference_in_percentages\n"
            results_wr.write(header)
            count = 0
            total_offset = 0
            sq_offset = 0
            for f, b in itertools.izip(real_Readercsv, predicted_val):
                # TODO: try to catch -1

                real_val = float(f[label])
                pred_val = float(b)
                abs_diff = abs(real_val - pred_val)
                dif_in_p = (pred_val * 100) / real_val
                String = "{0},{1},{2},{3:.2f}\n".format(
                    real_val, pred_val, abs_diff, dif_in_p)
                results_wr.write(String)
                count += 1
                total_offset += abs(float(f[label]) - float(b))
                sq_offset += abs(float(f[label]) - float(b))**2
                print sq_offset
            MSE = total_offset / count
            RMSE = numpy.sqrt(sq_offset / count)
            String = "----------------\n"
            String += "MAE: {0}\n".format(MSE)
            String += "RMSE: {0}\n".format(RMSE)
            print(String)

    except Exception, e:
        raise


if __name__ == '__main__':
    main(sys.argv[1:])
