import pandas as pd
import numpy as np
import operator

df = pd.read_csv("./Data/Mortality.csv")
df['px'] = 1 - df['qx']
parameters = {
    'df': df,
    'i': 0.035,
    'c': 0.025,
    'init_age': 26,
    'final_age': 100,
}


class PresentValueFutureExpenses(object):

    @classmethod
    def get_pvfe_dictionary(cls, parameters):
        (df, i, c, init_age, final_age) = cls.validate_parameters(**parameters)
        pvfe_dictionary = {}
        for age in range(init_age, final_age + 1):
            pvfe_dictionary[age] = cls.get_pvfe_for_specific_age(df, age, i, c)
        return(pvfe_dictionary)

    @classmethod
    def get_pvfe_for_specific_age(cls, df, age, i, c):
        df = cls.get_future_information_table_for_specific_retiring_age(df, age, i, c)
        pvfe = 0
        for k in range(0, len(df)):
            pvfe += df['npx'][k] * df['v_n'][k]
        return(pvfe)

    @classmethod
    def get_future_information_table_for_specific_retiring_age(cls, df, age, i, c):
        df, max_future_years = cls.clean_data_for_specific_age(df, age)
        df = cls.add_npx(df, max_future_years)
        df = cls.add_n_qx(df, max_future_years)
        df = cls.add_v_n(df, max_future_years, i, c)
        return(df)

    @staticmethod
    def clean_data_for_specific_age(df, age):
        df = df[df['x'] >= age].reset_index(drop=True)
        max_future_years = len(df)
        return(df, max_future_years)

    @staticmethod
    def add_npx(df, max_future_years):
        npx = [1]
        for k in range(1, max_future_years):
            npx.append(npx[-1] * df['px'][k - 1])
        df['npx'] = npx
        return(df)

    @staticmethod
    def add_n_qx(df, max_future_years):
        n_qx = []
        for k in range(0, max_future_years):
            n_qx.append(df['npx'][k] * df['qx'][k])
        df['n_qx'] = n_qx
        return(df)

    @staticmethod
    def add_v_n(df, max_future_years, i, c):
        v_n = []
        for k in range(0, max_future_years):
            v_n.append(((1 + c) / (1 + i)) ** float(k))
        df['v_n'] = v_n
        return(df)

    @staticmethod
    def validate_parameters(df, i, c, init_age, final_age):
        return (df, i, c, init_age, final_age)

    @staticmethod
    def product(iterable):
        return reduce(operator.mul, iterable, 1)
