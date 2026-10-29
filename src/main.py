import pandas as pd

# read csv file into pandas dataframe
df = pd.read_csv("../MetObjects.csv", 
                 dtype=str, 
                 skip_blank_lines=False, 
                 nrows=50, 
                 usecols=["Object Number", "Title", "Country"])

print(df.to_string(
    index=False,
    col_space={"Object Number": 14, "Title": 25, "Country":20},
    max_colwidth=45,
    justify="right",
    na_rep=""
))