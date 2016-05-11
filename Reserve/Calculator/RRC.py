import pandas as pd
import numpy as np

from ..Data.pvfe import base_pvfe

retired_group = pd.DataFrame({
    'id': [1, 2, 3, 4],
    'age': [45, 56, 72, 32],
    'retirement_age': [32, 40, 36, 29],
    'payment': [50, 100, 125, 150],
})

alpha = 0.30
qi_x = 0.001
c = 0.025


class RRC(object):

    @classmethod
    def get_group_BEL(cls, retired_group, c):
        retired_group = cls.add_retired_years(retired_group)
        retired_group = cls.add_accumulated_growth(retired_group, c)
        retired_group = cls.add_pvfe_column(retired_group)
        return((retired_group['payment'] * retired_group['accumulated_growth'] * retired_group['pvfe']).sum())

    @classmethod
    def add_accumulated_growth(cls, retired_group, c):
        retired_group['accumulated_growth'] = retired_group['retired_years'].apply(lambda x: cls.get_ag(x,c))
        return(retired_group)

    @classmethod
    def add_pvfe_column(cls, active_group):
        active_group['pvfe'] = active_group['age'].apply(cls.get_pvfe_for_specific_age)
        return(active_group)

    @staticmethod
    def add_retired_years(retired_group):
        retired_group['retired_years'] = retired_group['age'] - retired_group['retirement_age']
        return(retired_group)

    @staticmethod
    def get_ag(retired_years, c):
        return((1 + c) ** retired_years)

    @staticmethod
    def get_pvfe_for_specific_age(age):
        return(base_pvfe[age])
