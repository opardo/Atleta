import pandas as pd
import numpy as np

from ...Data.pvfe import base_pvfe
from ...Data.parameters import invalidity_alpha, qi_x
from ...Data.test import active_group


class InvalidityContributionCalculator(object):

    @classmethod
    def get_total_invalidity_contribution(
            cls,
            active_group=active_group,
            update=False,
            qi_x=qi_x,
            invalidity_alpha=invalidity_alpha):

        if update:
            active_group = cls.update_last_invalidity_contribution(
                active_group,
                qi_x,
                invalidity_alpha
            )

        return(active_group['invalidity_contribution'].sum())

    @classmethod
    def update_last_invalidity_contribution(
            cls,
            active_group=active_group,
            qi_x=qi_x,
            invalidity_alpha=invalidity_alpha):
        active_group['invalidity_contribution'] = qi_x * invalidity_alpha * active_group['salary'] * cls.pvfe_column(active_group)
        active_group.loc[active_group['age'] < 26, 'invalidity_contribution'] = 0
        return(active_group)

    @classmethod
    def pvfe_column(cls, active_group):
        return(active_group['age'].apply(cls.get_pvfe_for_specific_age))

    @staticmethod
    def get_pvfe_for_specific_age(age):
        return(base_pvfe[age])
