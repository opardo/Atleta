import pandas as pd
import numpy as np

from ...Data.pvfe import base_pvfe
from ...Data.parameters import invalidity_alpha, qi_x
from ...Data.test import active_group


class RRCI(object):

    @classmethod
    def get_group_BEL(
            cls,
            active_group=active_group,
            invalidity_alpha=invalidity_alpha,
            qi_x=qi_x,
            pvfe=base_pvfe):

        active_group = cls.add_pvfe_column(active_group, pvfe)

        return(qi_x * invalidity_alpha * (active_group['salary'] * active_group['pvfe']).sum())

    @classmethod
    def add_pvfe_column(cls, active_group, pvfe):
        active_group['pvfe'] = active_group['age'].apply(lambda x: cls.get_pvfe_for_specific_age(x, pvfe))
        return(active_group)

    @staticmethod
    def get_pvfe_for_specific_age(age, pvfe):
        return(pvfe[age])
