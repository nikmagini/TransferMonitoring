"""
File       : jsonUtilities.py
Author     : Zygimantas Matonis
Description: Read csv and slit to random train/test files given filenames and ratio
"""

# import csv
import sys
import getopt  # http://www.tutorialspoint.com/python/python_command_line_arguments.htm
import random
from itertools import islice


def main(argv):
    """Main function"""
    percent = 66  # percentage size of train file
    inputfile = ''
    out_test = "/tmp/test.csv"
    out_train = "/tmp/train.csv"

    message = 'csvSplit.py -i <inputfile> -otrain <outputfile> '
    message += '-otest <outputfile> -p <train percentage>'
    try:
        opts, args = getopt.getopt(
            argv, "hi:p:", ["ifile=", "otrain=", "otest="])
    except getopt.GetoptError:
        print(message)
        sys.exit(2)
    for opt, arg in opts:
        if opt == '-h':
            print(message)
            sys.exit(2)
        elif opt in ("-i", "--ifile"):
            inputfile = arg
        elif opt in ("--otrain"):
            out_train = arg
        elif opt in ("--otest"):
            out_test = arg
        elif opt in ("-p"):
            percent = int(arg)
            # --------------------------------

    try:
        with open(inputfile, 'r') as source, \
                open(out_test, 'w') as test_f, \
                open(out_train, 'w') as train_f:

            header = source.readline()
            test_f.write(header)
            train_f.write(header)

            while True:
                next_n_lines = list(islice(source, 1000))
                if not next_n_lines:
                    break
                random.shuffle(next_n_lines)
                split_point = int(len(next_n_lines) * (percent / float(100)))
                trainList = next_n_lines[:split_point]
                testList = next_n_lines[split_point:]
                test_f.writelines(trainList)
                train_f.writelines(testList)

    except Exception, e:
        raise e
        print("something was wrong")
        sys.exit(2)


if __name__ == '__main__':
    main(sys.argv[1:])
