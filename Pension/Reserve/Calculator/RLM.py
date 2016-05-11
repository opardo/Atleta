import pandas as pd
import numpy as np

from ...Data.test import active_group, base_mortality


class RLM(object):

    @classmethod
    def get_group_BEL(
            cls,
            active_group=active_group,
            mortality=base_mortality):

        active_group = cls.add_qx_column(active_group, mortality)

        return((active_group['IA'] * active_group['qx']).sum())

    @classmethod
    def add_qx_column(cls, active_group, mortality):
        active_group['qx'] = active_group['age'].apply(lambda x: cls.get_qx(x, mortality))
        return(active_group)

    @staticmethod
    def get_qx(age, mortality):
        return(base_mortality[age])
