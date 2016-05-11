import pandas as pd
import numpy as np

from ...Data.pvfe import base_pvfe
from ...Data.parameters import g
from ...Data.test import retired_group


class RRC(object):

    @classmethod
    def get_group_BEL(
            cls,
            retired_group=retired_group,
            g=g):

        retired_group = cls.add_retired_years(retired_group)
        retired_group = cls.add_accumulated_growth(retired_group, g)
        retired_group = cls.add_pvfe_column(retired_group)

        return((retired_group['payment'] * retired_group['accumulated_growth'] * retired_group['pvfe']).sum())

    @classmethod
    def add_accumulated_growth(cls, retired_group, g):
        retired_group['accumulated_growth'] = retired_group['retired_years'].apply(lambda x: cls.get_ag(x, g))
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
    def get_ag(retired_years, g):
        return((1 + g) ** retired_years)

    @staticmethod
    def get_pvfe_for_specific_age(age):
        return(base_pvfe[age])
