import pandas as pd
import numpy as np

from ...Data.pvfe import base_pvfe
from ...Data.parameters import g
from ...Data.test import retired_group


class RMR(object):

    @classmethod
    def get_group_BEL(
            cls,
            retired_group=retired_group,
            g=g):
        retired_group = cls.add_accumulated_growth(retired_group, g)
        return((retired_group['IA_pension'] * retired_group['accumulated_growth'] * retired_group['pvfe']).sum())

    @classmethod
    def add_accumulated_growth(cls, retired_group, g):
        retired_group['accumulated_growth'] = retired_group['retired_years'].apply(lambda x: cls.get_ag(x, g))
        return(retired_group)

    @staticmethod
    def get_ag(retired_years, g):
        return((1 + g) ** retired_years)
