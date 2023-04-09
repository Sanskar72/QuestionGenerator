import pandas as pd
import numpy as np
from random import choice

def do(numQ):
    df = pd.read_csv('https://raw.githubusercontent.com/dev7796/data101_tutorial/main/files/dataset/airbnb.csv')
    #Lets set NaN name to "Unkown" and NaN host_name to "Unknown" as well. Fill NaN values with "Unknown"
    df.fillna('Unknown', inplace=True)
    
    data = []
    for i in range(int(numQ)):
        numerical = list(df.select_dtypes(np.number).columns)
        numerical.remove('id')
        categorical = list(df.select_dtypes(exclude = np.number).columns)
        aggregate = ["count", "sum", "mean", "median", "min", "max", "mode", "standard deviation", "variance"]
        n = choice(np.arange(len(categorical)-2)) + 1
        a = choice(numerical)
        c = choice(aggregate)
        text = "What is " + c + " of " + a + " when "
        for j in range(n):
            b = choice(categorical)
            text += b + " = '" + choice(df[b].unique()) + "' "
            categorical.remove(b)
            if j < n - 1:
                text += "and "
                
        data.append((i+1, text))


    return data


