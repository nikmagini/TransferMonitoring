#!/usr/bin/env python
"""
File       : jsonUtilities.py
Author     : Zygimantas Matonis
Description: Python 2.7 script to check predicted data with actual values
             and calculate MAE and RMSE. Used only for Regresion values.
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
    predictFile = '/tmp/predict.txt'
    realFiles = '/tmp/test.csv'
    resultsFile = '/tmp/check_results.txt'

    # predictFile = None
    # realFiles = None
    resultsFile = None

    label = 'timestamp_tr_dlt'

    message = 'checkPredictions.py --ireal <inputfile> --ipred <inputfile>'
    message += ' --ofile <output> --label <label>\n\n'

    l_message = '--ireal <inputfile>: csv file on which predictions where made\n'
    l_message += '--label <label>: name of predicted atributes\n'
    l_message += '--ipred <inputfile>: .txt file with 1 column of predicted values\n'
    l_message += '[optional] --ofile <output>: if this option given, output is created\n'
    l_message += 'that compares real values with predicted row by row\n\n'
    l_message += 'example of script with default parameters:\n'
    l_message += '\tcheckPredictions.py --ireal /tmp/test.csv '
    l_message += '--ipred /tmp/predict.txt --label timestamp_tr_dlt '
    l_message += '--ofile /tmp/check_results.txt'

    try:
        opts, args = getopt.getopt(
            argv, "h", ["ireal=", "ofile=", "ipred=", "label="])
    except getopt.GetoptError:
        print(message)
        print(l_message)
        sys.exit(2)
    for opt, arg in opts:
        if opt == '-h':
            print(message)
            print(l_message)
            sys.exit(2)
        elif opt in ("--ireal"):
            realFiles = arg
        elif opt in ("--ipred"):
            realFiles = arg
        elif opt in ("--ofile"):
            resultsFile = arg
        elif opt in ("--label"):
            label = arg
# ------------------------------------

    # check if input exsists
    # if((predictFile is None) or (realFiles is None)):
    #     print(message)
    #     sys.exit(2)

    try:
        with open(predictFile, 'r') as predicted_val, \
                open(realFiles, 'r') as real_val:

            real_Readercsv = csv.DictReader(real_val)
            predicted_val.readline()
            if (resultsFile):
                results_wr = open(resultsFile, 'w')
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

                if (resultsFile):
                    String = "{0},{1},{2},{3:.2f}\n".format(
                        real_val, pred_val, abs_diff, dif_in_p)
                    results_wr.write(String)

                count += 1
                total_offset += abs(float(f[label]) - float(b))
                sq_offset += abs(float(f[label]) - float(b))**2

            MSE = total_offset / count
            RMSE = numpy.sqrt(sq_offset / count)
            String = "----------------\n"
            String += "MAE: {0}\n".format(MSE)
            String += "RMSE: {0}\n".format(RMSE)
            print(String)

            if (resultsFile):
                results_wr.close

    except Exception as e:
        raise e

if __name__ == '__main__':
    main(sys.argv[1:])
