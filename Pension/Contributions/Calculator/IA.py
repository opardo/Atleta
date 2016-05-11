import pandas as pd
import numpy as np

from ...Data.parameters import IA_alpha
from ...Data.test import active_group


class IAContributionCalculator(object):

    @classmethod
    def get_total_IA(
            cls,
            active_group=active_group,
            update=False,
            IA_alpha=IA_alpha):

        if update:
            active_group = cls.update_group_IA(active_group, IA_alpha)

        return(active_group['IA'].sum())

    @classmethod
    def get_total_last_IA_contribution(
            cls,
            active_group=active_group,
            update=False,
            IA_alpha=IA_alpha):

        if update:
            active_group = cls.update_group_IA(active_group, IA_alpha)

        return(active_group['IA_contribution'].sum())

    @classmethod
    def update_group_IA(
            cls,
            active_group=active_group,
            IA_alpha=IA_alpha):

        active_group = cls.update_last_IA_contribution(active_group, IA_alpha)
        active_group = cls.update_individual_IA(active_group)

        return(active_group)

    @staticmethod
    def update_last_IA_contribution(active_group, IA_alpha):
        active_group['IA_contribution'] = IA_alpha * active_group['salary']
        return(active_group)

    @staticmethod
    def update_individual_IA(active_group):
        active_group['IA'] = active_group['IA'] + active_group['IA_contribution']
        return(active_group)

