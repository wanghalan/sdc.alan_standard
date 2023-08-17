from ast import Str
from logging import root
import pathlib
import pandas as pd
from tqdm import tqdm
import re
import argparse
import os
from pprint import pprint

'''
Check that all data files follow the following convention:
    1) <year>_<fips_code>_<measure_name>_<number_of_rows>.csv.xz
'''

_DATA_PATH_PATTERN = '**/data/distribution/*.csv.xz'
_VALID_DATA_FILE_NAME_PATTERN = r"[0-9]{4},[0-9]{2,15},[a-z_]{1,},[0-9]{1,}.csv.xz$"


def dir_path(path):
    if os.path.isdir(path):
        return path
    else:
        raise argparse.ArgumentTypeError(f"readable_dir:{path} is not a valid path")



def set_up_argparse():
    parser = argparse.ArgumentParser("Validate data file name standard")
    parser.add_argument("-r", "--root_dir", help="Directory to check that ", required=True,
                type=dir_path)
    args = parser.parse_args()
    return args


def main(root_dir):
    data_files = sorted(pathlib.Path(root_dir).glob(_DATA_PATH_PATTERN))
    if len(data_files) <= 0:
        print('No files math in %s' % pathlib.Path(root_dir).resolve())
        return

    pbar = tqdm(data_files)
    valid_files = []
    valid_count = 0
    for file in pbar:
        valid =  bool(re.search(_VALID_DATA_FILE_NAME_PATTERN, file.name))
        valid_files.append([str(file.resolve()),valid])
        if valid:
            valid_count += 1

    pprint(valid_files)
    compliance_perc = (valid_count/ len(valid_files) * 100)
    print('-'*80)
    print('Total compliance percentage: %.2f%%' %compliance_perc)
    assert compliance_perc == 100
    
if __name__ == "__main__":
    args = set_up_argparse()

    main(args.root_dir)
