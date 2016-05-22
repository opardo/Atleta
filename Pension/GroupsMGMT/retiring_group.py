import pandas as pd
import numpy as np

from ..Data.test import active_group
from ..Data.parameters import invalidity_alpha
from ..Data.retiring_probabilities import base_retiring_reasons_probabilities
from ..Data.mortality_probabilities import base_mortality
from ..Data.pvfe import base_pvfe
from ..shared import add_qx_column, add_pvfe_column


class UpdateRetiringGroup(object):

    @classmethod
    def update(cls, volunteer_group, invalid_group, mortality=base_mortality):
        volunteer_group = cls.update_group(volunteer_group, mortality)
        invalid_group = cls.update_group(invalid_group, mortality)
        return(volunteer_group, invalid_group)

    @classmethod
    def update_group(cls, group, mortality):
        group = cls.drop_columns(group)
        group = cls.rename_columns(group)
        group = cls.add_columns(group, mortality)
        return(group)

    @staticmethod
    def rename_columns(group):
        group = group.rename(columns={'salary': 'last_salary'})
        return(group)

    @staticmethod
    def add_columns(group, mortality):
        group['retirement_age'] = group['age']
        group['retired_years'] = len(group) * [0]
        group = add_qx_column(group, mortality)
        return(group)

    @staticmethod
    def drop_columns(group):
        return(
            group.drop(['IA', 'IA_contribution', 'invalidity_contribution', 'qx'], axis=1)
        )


class CalculatePensions(object):

    @staticmethod
    def get_generation_this_year_IA_pension(volunteer_group, invalid_group):
        return(volunteer_group['IA_pension'].sum() + invalid_group['IA_pension'].sum())

    @staticmethod
    def get_generation_this_year_invalid_pension(invalid_group):
        return(invalid_group['invalidity_pension'].sum())

    @staticmethod
    def get_pvfe_IA_generation(volunteer_group, invalid_group):
        return(volunteer_group['IA'].sum() + invalid_group['IA'].sum())

    @staticmethod
    def get_pvfe_invalid_generation(invalid_group):
        return((invalid_group['pvfe'] * invalid_group['invalidity_pension']).sum())

    @classmethod
    def calculate_invalid_and_volunteer_groups_pensions(cls,
                                                        volunteer_group,
                                                        invalid_group,
                                                        pvfe=base_pvfe):
        volunteer_group = cls.calculate_pension(volunteer_group, False, pvfe)
        invalid_group = cls.calculate_pension(invalid_group, True, pvfe)
        return(volunteer_group, invalid_group)

    @classmethod
    def calculate_pension(cls, group, invalidity, pvfe):
        group = cls.calculate_IA_pension(group, pvfe)
        group = cls.calculate_invalidity_pension(group, invalidity_alpha, invalidity)
        return(group)

    @classmethod
    def calculate_IA_pension(cls, group, pvfe):
        group['age'] = group['age'] + 1
        group = add_pvfe_column(group, pvfe)
        group['IA_pension'] = group['IA'] / (group['pvfe'])
        return(group)

    @classmethod
    def calculate_invalidity_pension(cls, group, invalidity_alpha, invalidity=True):
        if invalidity:
            group['invalidity_pension'] = invalidity_alpha * group['salary']
        else:
            group['invalidity_pension'] = len(group) * [0]
        return(group)


class RetiringReason(object):

    @classmethod
    def simulate_retiring_reasons_groups(cls,
                                         retiring_group=active_group,
                                         retiring_reasons_probabilities=base_retiring_reasons_probabilities):
        retiring_group = cls.add_retiring_reasons(
            retiring_group,
            retiring_reasons_probabilities
        )
        print retiring_group
        if retiring_group.empty:
            volunteer_group = retiring_group[retiring_group['retiring_reason']=='v']
            death_group = retiring_group[retiring_group['retiring_reason']=='d']
            invalid_group = retiring_group[retiring_group['retiring_reason']=='i']
        else:
            volunteer_group = retiring_group
            death_group = retiring_group
            invalid_group = retiring_group

        return(
            volunteer_group.drop('retiring_reason', 1),
            death_group.drop('retiring_reason', 1),
            invalid_group.drop('retiring_reason', 1)
        )

    @classmethod
    def add_retiring_reasons(cls,
                             retiring_group,
                             retiring_reasons_probabilities):
        retiring_group['retiring_reason'] = retiring_group['age'].apply(lambda x: cls.get_retiring_reason_by_age(x, retiring_reasons_probabilities))
        return(retiring_group)

    @staticmethod
    def get_retiring_reason_by_age(x, retiring_reasons_probabilities):
        qxv = retiring_reasons_probabilities[x]['v']
        qxd = retiring_reasons_probabilities[x]['d']
        simulation = np.random.rand()
        if simulation <= qxv:
            return('v')
        elif simulation <= (qxv + qxd):
            return('d')
        else:
            return('i')




