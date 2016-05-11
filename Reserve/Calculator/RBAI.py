import pandas as pd
import numpy as np

from ..Data.pvfe import base_pvfe

active_group = pd.DataFrame({
    'id': [1, 2, 3, 4],
    'age': [31, 37, 33, 29],
    'IA': [1000, 2000, 3000, 4000],
    'salary': [200, 400, 500, 600]
})

invalid_group = pd.DataFrame({
    'id': [1, 2, 3, 4],
    'age': [45, 56, 72, 32],
    'retirement_age': [32, 40, 36, 29],
    'last_salary': [200, 400, 500, 600]
})

alpha = 0.30
qi_x = 0.001
c = 0.025


class RBAI(object):

    @classmethod
    def get_group_BEL(cls, active_group, invalid_group, alpha, qi_x, c):
        not_invalid_BEL = cls.get_not_invalid_BEL(active_group, alpha, qi_x)
        invalid_BEL = cls.get_invalid_BEL(invalid_group, c)
        return(not_invalid_BEL + invalid_BEL)

    @classmethod
    def get_not_invalid_BEL(cls, active_group, alpha, qi_x):
        active_group = cls.add_pvfe_column(active_group)
        return(alpha * qi_x * (active_group['salary'] * active_group['pvfe']).sum())

    @classmethod
    def get_invalid_BEL(cls, invalid_group, c):
        invalid_group = cls.add_todays_salary(invalid_group, c)
        invalid_group = cls.add_pvfe_column(invalid_group)
        return(alpha * (invalid_group['todays_salary'] * invalid_group['pvfe']).sum())

    @classmethod
    def add_pvfe_column(cls, active_group):
        active_group['pvfe'] = active_group['age'].apply(cls.get_pvfe_for_specific_age)
        return(active_group)

    @classmethod
    def add_todays_salary(cls, invalid_group, c):
        invalid_group = cls.add_retired_years(invalid_group)
        invalid_group = cls.add_accumulated_growth(invalid_group, c)
        invalid_group['todays_salary'] = invalid_group['last_salary'] * invalid_group['accumulated_growth']
        return(invalid_group)

    @classmethod
    def add_accumulated_growth(cls, invalid_group, c):
        invalid_group['accumulated_growth'] = invalid_group['retired_years'].apply(lambda x: cls.get_ag(x,c))
        return(invalid_group)

    @staticmethod
    def add_retired_years(invalid_group):
        invalid_group['retired_years'] = invalid_group['age'] - invalid_group['retirement_age']
        return(invalid_group)

    @staticmethod
    def get_ag(retired_years, c):
        return((1 + c) ** retired_years)

    @staticmethod
    def get_pvfe_for_specific_age(age):
        return(base_pvfe[age])
