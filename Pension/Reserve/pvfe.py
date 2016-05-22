import pandas as pd
import numpy as np
import operator

from ..Data.parameters import i, g, init_age, final_age

df = pd.read_csv("Pension/Data/CSV/Mortality.csv")
df['px'] = 1 - df['qx']


class PresentValueFutureExpenses(object):

    @classmethod
    def get_pvfe_dictionary(cls,
                            df=df,
                            i=i,
                            c=g,
                            init_age=init_age,
                            final_age=final_age):

        pvfe_dictionary = {}
        for age in range(init_age, final_age + 1):
            pvfe_dictionary[age] = cls.get_pvfe_for_specific_age(df, age, i, c)
        return(pvfe_dictionary)

    @classmethod
    def get_pvfe_for_specific_age(cls, df, age, i, c):
        df = cls.get_future_information_table_for_specific_retiring_age(df, age, i, c)
        return((df['npx'] * df['v_n']).sum())

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
    def product(iterable):
        return reduce(operator.mul, iterable, 1)
