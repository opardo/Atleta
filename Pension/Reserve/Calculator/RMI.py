import pandas as pd
import numpy as np

from ...Data.pvfe import base_pvfe
from ...Data.parameters import invalidity_alpha, g
from ...Data.test import invalid_group


class RMI(object):

    @classmethod
    def get_group_BEL(
            cls,
            invalid_group=invalid_group,
            invalidity_alpha=invalidity_alpha,
            g=g,
            pvfe=base_pvfe):

        invalid_group = cls.add_todays_salary(invalid_group, g)
        invalid_group = cls.add_pvfe_column(invalid_group, pvfe)

        return(invalidity_alpha * (invalid_group['todays_salary'] * invalid_group['pvfe']).sum())

    @classmethod
    def add_todays_salary(cls, invalid_group, g):
        invalid_group = cls.add_retired_years(invalid_group)
        invalid_group = cls.add_accumulated_growth(invalid_group, g)
        invalid_group['todays_salary'] = invalid_group['last_salary'] * invalid_group['accumulated_growth']
        return(invalid_group)

    @classmethod
    def add_pvfe_column(cls, active_group, pvfe):
        active_group['pvfe'] = active_group['age'].apply(lambda x: cls.get_pvfe_for_specific_age(x, pvfe))
        return(active_group)

    @classmethod
    def add_accumulated_growth(cls, invalid_group, g):
        invalid_group['accumulated_growth'] = invalid_group['retired_years'].apply(lambda x: cls.get_ag(x, g))
        return(invalid_group)

    @staticmethod
    def add_retired_years(invalid_group):
        invalid_group['retired_years'] = invalid_group['age'] - invalid_group['retirement_age']
        return(invalid_group)

    @staticmethod
    def get_ag(retired_years, g):
        return((1 + g) ** retired_years)

    @staticmethod
    def get_pvfe_for_specific_age(age, pvfe):
        return(pvfe[age])
