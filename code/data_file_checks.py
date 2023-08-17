import re
import os
import pandas as pd


def has_valid_file_name(posix, data_standard):
    return bool(re.search(data_standard["VALID_DATA_FILE_NAME_PATTERN"], posix.name))


def has_valid_data_column_names(posix, data_standard):
    if not os.path.isfile(posix):
        return False
    geo_cols = data_standard["GEOID_COLS"]
    # reading these columns as strings
    dtype = {}
    for g in geo_cols:
        dtype[g] = object
    df = pd.read_csv(posix, dtype=dtype)
    df_cols = set(df.columns)
    req_cols = set(data_standard["REQUIRED_COL_NAMES"])

    if len(req_cols - df_cols) != 0:
        print()
        return False

    return True


def has_no_empty_geoid_rows(posix, data_standard):
    if not os.path.isfile(posix):
        return False
    geo_cols = data_standard["GEOID_COLS"]
    # reading these columns as strings
    dtype = {}
    for g in geo_cols:
        dtype[g] = object
    df = pd.read_csv(posix, dtype=dtype)

    ddf = df.dropna(geo_cols, axis=1)
    if len(df) != len(ddf):
        return False

    for g in geo_cols:
        if not g in df.columns:
            return False

    return True


def main():
    return {
        "VALID_DATA_FILE_NAME_PATTERN": has_valid_file_name,
        "REQUIRED_COL_NAMES": has_valid_data_column_names,
        "GEOID_PATTERN": has_no_empty_geoid_rows,
    }
