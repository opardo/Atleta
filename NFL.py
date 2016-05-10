import pandas as pd
import numpy as np
import operator

df = pd.read_csv("./Downloads/MortalidadNFL.csv")
df['px'] = 1 - df['qx']

def get_information_table_for_specific_retiring_age(df, age):
    df = df[df['x']>=age].reset_index(drop=True)
    df.index += 1
    max_future_years = len(df)
    npx = [1]
    for k in range(2, max_future_years+1):
        npx.append(prod(df[:(k-1)]['px']))
    df['npx'] = npx
    n_qx = []
    for k in range(1, max_future_years+1):
        n_qx.append(df['npx'][k]*df['qx'][k])
    df['n_qx'] = n_qx
    p_alive = [1]
    for k in range(2, max_future_years+1):
        p_alive.append(p_alive[-1]*df['px'])
    df['n_qx'] = n_qx
    # TO DO: Adjust for different interest rates
    i =  0.03
    v_n = []
    for k in range(1, max_future_years+1):
        v_n.append((1+i)**float(-(k-1)))
    df['v_n'] = v_n
    return df

def prod(iterable):
    return reduce(operator.mul, iterable, 1)
