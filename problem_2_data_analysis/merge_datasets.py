import pandas as pd
import numpy as np
import os

if __name__ == "__main__":
    datasets = [
        'data/1_2015.csv',
        'data/2_2015.csv',
        'data/1_2016.csv',
        'data/1_2017.csv',
        'data/2_2017.csv',
        'data/2_2016.csv']

    df = dict({os.path.basename(d).split(".")[0]: pd.read_csv("problem_2_data_analysis/"+d) for
               d in datasets})

    for k, df_year in df.items():
        df_year["Dataset"] = k

    df_merge = pd.concat(df.values())
