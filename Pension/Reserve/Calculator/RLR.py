import pandas as pd
import numpy as np

from ...Data.retiring_probabilities import base_retiring
from ...Data.test import active_group


class RLR(object):

    @classmethod
    def get_group_BEL(
            cls,
            active_group=active_group,
            retiring=base_retiring):

        active_group = cls.add_qx_column(active_group, retiring)

        return((active_group['IA'] * active_group['qx']).sum())

    @classmethod
    def add_qx_column(cls, active_group, retiring):
        active_group['qx'] = active_group['age'].apply(lambda x: cls.get_qx(x, retiring))
        return(active_group)

    @staticmethod
    def get_qx(age, retiring):
        return(float(retiring[str(age)]))
