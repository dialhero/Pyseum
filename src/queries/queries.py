import pandas as pd

def print_first_five_rows(df):
    return df.head()

def filter_for_index_loc(df, row):
    return df.iloc[row]

def filter_for_header_and_specified_object(df, header_name, object_name):
    return df[df[header_name] == object_name]