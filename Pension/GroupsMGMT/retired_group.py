import pandas as pd
import numpy as np

from ..Data.test import retired_group
from ..Data.parameters import g
from ..Data.mortality_probabilities import base_mortality
from ..Data.pvfe import base_pvfe
from ..Data.survival_probabilities import base_tPx
from ..Data.forward import Forward
from ..shared import add_qx_column, add_pvfe_column, add_tPx_column


class RetiredInvestment(object):

    @staticmethod
    def update_D_vector(D, iv, year):
        D = D[1:]
        D = np.append(D, [0])
        x = []
        for k in range(0, len(iv)):
            x.append(float(iv[k] * (1 + Forward[year][k + 1]) ** (k + 1)))
        x = np.array(x)
        D = D + x
        return(D)

    @classmethod
    def get_obligations_vector(cls, retired_group, pension, tPx_dict=base_tPx):
        retired_group = cls.add_accumulated_growth(retired_group, g)
        retired_group = add_tPx_column(retired_group, tPx_dict)
        return((retired_group['accumulated_growth'] * retired_group[pension] * retired_group['tPx']).sum())

    @classmethod
    def get_O0(cls, retired_group, pension):
        retired_group = cls.add_accumulated_growth(retired_group, g)
        return((retired_group['accumulated_growth'] * retired_group[pension]).sum())

    @staticmethod
    def get_CRN_and_R0(D0, O0):
        if D0 > O0:
            CRN = 0
            R0 = D0 - O0
        else:
            CRN = O0 - D0
            R0 = 0
        return(CRN, R0)

    @classmethod
    def add_accumulated_growth(cls, retired_group, g):
        retired_group['accumulated_growth'] = retired_group['retired_years'].apply(lambda x: cls.get_ag(x, g))
        return(retired_group)

    @staticmethod
    def get_ag(retired_years, g):
        return((1 + g) ** retired_years)


class UpdateRetiredGroup(object):

    @staticmethod
    def add_new_retired(retired_group, volunteer_group, invalid_group):
        retired_group = retired_group.append(volunteer_group)
        retired_group = retired_group.append(invalid_group)
        return(retired_group)

    @staticmethod
    def update_past_retired(retired_group=retired_group, mortality=base_mortality, pvfe=base_pvfe):
        retired_group['age'] = retired_group['age'] + 1
        retired_group['retired_years'] = retired_group['retired_years'] + 1
        retired_group = add_qx_column(retired_group, mortality)
        retired_group = add_pvfe_column(retired_group, pvfe)
        return(retired_group)



class MortalityRetiredGroup(object):

    @staticmethod
    def simulate_mortality(retired_group=retired_group):
        retired_group['qx'] = pd.to_numeric(retired_group['qx'], errors='coerce')
        initial = len(retired_group)
        retired_group['simulation'] = np.random.rand(len(retired_group))
        retired_group = retired_group[retired_group['simulation'] >= retired_group['qx']]
        final = len(retired_group)
        return(retired_group.drop('simulation', 1), initial - final)
