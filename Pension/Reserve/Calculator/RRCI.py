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
        active_group = active_group[active_group['age'] >= 26]
        return(qi_x * invalidity_alpha * (active_group['salary'] * active_group['pvfe']).sum())
