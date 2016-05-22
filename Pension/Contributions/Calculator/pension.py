import pandas as pd
import numpy as np

from ...Data.pvfe import base_pvfe
from ...Data.parameters import invalidity_alpha
from ...Data.test import active_group, volunteer_ids, invalidity_ids, death_ids


class PensionCalculator(object):

    @classmethod
    def add_Pension(cls,
                    active_group=active_group,
                    volunteer_ids=volunteer_ids,
                    invalidity_ids=invalidity_ids,
                    death_ids=death_ids):

        (
            active_group,
            volunteer_group,
            death_group,
            invalidity_group,
        ) = cls.get_groups(active_group, volunteer_ids, invalidity_ids, death_ids)
        volunteer_group = cls.calculate_pension(volunteer_group, False)
        invalidity_group = cls.calculate_pension(invalidity_group, True)
        return(active_group, volunteer_group, death_group, invalidity_group)

    @classmethod
    def calculate_pension(cls, group, invalidity):
        group = cls.add_pvfe_column(group)
        group = cls.calculate_IA_pension(group)
        group = cls.calculate_invalidity_pension(group, invalidity_alpha, invalidity)
        return(group)

    @classmethod
    def calculate_IA_pension(cls, group):
        group['IA_pension'] = group['IA'] / group['pvfe']
        return(group)

    @classmethod
    def calculate_invalidity_pension(cls, group, invalidity_alpha=invalidity_alpha, invalidity=True):
        if invalidity:
            group['invalidity_pension'] = invalidity_alpha * group['salary']
        else:
            group['invalidity_pension'] = len(group) * [0]
        return(group)

    @classmethod
    def add_pvfe_column(cls, group):
        group['pvfe'] = group['age'].apply(cls.get_pvfe_for_specific_age)
        return(group)

    @staticmethod
    def get_pvfe_for_specific_age(age):
        return(base_pvfe[age])

    @staticmethod
    def get_groups(active_group, volunteer_ids, invalidity_ids, death_ids):

        volunteer_group = active_group[active_group['id'].isin(volunteer_ids)]
        death_group = active_group[active_group['id'].isin(death_ids)]
        invalidity_group = active_group[active_group['id'].isin(invalidity_ids)]
        retiring_ids = list(set(volunteer_ids + invalidity_ids + death_ids))
        active_group = active_group.drop(active_group[active_group['id'].isin(retiring_ids)].index)

        return(active_group, volunteer_group, death_group, invalidity_group)

