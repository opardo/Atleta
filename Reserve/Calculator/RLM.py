import pandas as pd
import numpy as np

base_mortality = pd.read_csv("./Data/Mortality.csv")

active_group = pd.DataFrame({
    'id': [1, 2, 3, 4],
    'age': [31, 37, 33, 29],
    'IA': [1000, 2000, 3000, 4000],
})


class RLM(object):

    @classmethod
    def get_group_BEL(cls, active_group):
        active_group = cls.add_qx_column(active_group)
        return((active_group['IA'] * active_group['qx']).sum())

    @classmethod
    def add_qx_column(cls, active_group):
        active_group['qx'] = active_group['age'].apply(cls.get_qx)
        return(active_group)

    @staticmethod
    def get_qx(age):
        age_base_mortality_row = base_mortality[base_mortality['x'] == age].reset_index(drop=True)
        return(age_base_mortality_row.at[0, 'qx'])
