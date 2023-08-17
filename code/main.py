from ast import Str
from logging import root
import pathlib
import pandas as pd
from tqdm import tqdm
import re
import argparse
import os
from pprint import pprint
import json
from data_file_checks import main as check_main

"""
Check that all data files follow the following convention:
    1) <year>_<fips_code>_<measure_name>_<number_of_rows>.csv.xz
"""


def dir_path(path):
    if os.path.isdir(path):
        return path
    else:
        raise argparse.ArgumentTypeError(f"readable_dir:{path} is not a valid path")


def set_up_argparse():
    parser = argparse.ArgumentParser("Validate data file name standard")
    parser.add_argument(
        "-r",
        "--root_dir",
        help="Directory to check that ",
        required=True,
        type=dir_path,
    )
    args = parser.parse_args()
    return args


def main(root_dir):
    # Loading in default data standards
    data_standard = {}
    default_standard = os.path.join(
        os.path.dirname(os.path.abspath(__file__)), "data_standard.json"
    )
    with open(default_standard, "r") as f:
        data_standard = json.load(f)

    expected_custom_data_standard_location = os.path.join(
        root_dir, ".data_standard.json"
    )
    if os.path.isfile(expected_custom_data_standard_location):
        with open(expected_custom_data_standard_location, "r") as f:
            custom_data_standard = json.load(f)
            # Override all existing defaults, but not all of them
            for key in custom_data_standard:
                if key in data_standard:
                    data_standard[key] = custom_data_standard[key]

    pprint(data_standard)
    input("Confirm standards? Press enter to continue...")
    data_files = [
        f
        for f in sorted(pathlib.Path(root_dir).glob(data_standard["DATA_PATH_PATTERN"]))
        if os.path.isfile(f)  # because it is possible to name a directory .csv.xz
    ]
    if len(data_files) <= 0:
        print("No files math in %s" % pathlib.Path(root_dir).resolve())
        return

    pbar = tqdm(data_files)
    valid_files = []
    valid_count = 0
    for file in pbar:
        pbar.set_description("Validating: %s" % str(file.resolve()))
        checks = check_main()

        final_status = True
        for k in checks:
            if not k in data_standard:
                continue
            valid = checks[k](file, data_standard)
            if not valid:
                print("\tChecking {key}, status: {status}".format(key=k, status=valid))
            final_status = final_status and valid
        if final_status:
            valid_count += 1
        valid_files.append([str(file.resolve()), final_status])

    # pprint(valid_files)
    compliance_perc = valid_count / len(valid_files) * 100
    print("-" * 80)
    print("Total compliance percentage: %.2f%%" % compliance_perc)
    return compliance_perc == 100


if __name__ == "__main__":
    args = set_up_argparse()

    main(args.root_dir)
