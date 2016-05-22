import pandas as pd
import numpy as np

from ..Data.test import active_group, last_ID
from ..Data.parameters import players_number, shape, scale, loc, sg, qi_x, invalidity_alpha, IA_alpha, promised_yield, yield_comission_rate, GA, MU
from ..Data.retiring_probabilities import base_retiring
from ..shared import add_pvfe_column, add_qx_column
from ..Contributions.Calculator.IA import IAContributionCalculator
from ..Contributions.Calculator.invalidity import InvalidityContributionCalculator


class RetiringActiveGroup(object):

    @staticmethod
    def simulate_retirement(active_group=active_group):
        active_group['simulation'] = np.random.rand(len(active_group))
        retiring_group = active_group[active_group['simulation'] <= active_group['qx']]
        retiring_group = retiring_group[retiring_group['age'] >= 26]
        active_group = active_group[active_group['simulation'] > active_group['qx']]
        return(active_group.drop('simulation', 1), retiring_group.drop('simulation', 1))


class UpdateActiveGroup(object):

    @staticmethod
    def get_yield_commissions(active_group):
        IA_contributions = IAContributionCalculator.get_total_IA(active_group)
        return(IA_contributions * promised_yield * yield_comission_rate)

    @staticmethod
    def get_premium_rate(active_group=active_group, GA=GA, MU=MU):
        IA_contribution = IAContributionCalculator.get_total_last_IA_contribution(
            active_group
        )
        invalidity_contribution = InvalidityContributionCalculator.get_total_invalidity_contribution(
            active_group
        )
        return((IA_contribution + invalidity_contribution) / (1 - GA - MU))

    @staticmethod
    def update_yield_IA(active_group):
        active_group['IA'] = (1 + promised_yield * (1 - yield_comission_rate)) * active_group['IA']
        return(active_group)

    @classmethod
    def starting_update(cls,
                        active_group=active_group,
                        retiring=base_retiring,
                        players_number=players_number,
                        year=0,
                        last_ID=last_ID,
                        qi_x=qi_x):
        active_group = cls.next_year_basic_update(
            active_group,
            players_number,
            year,
            last_ID,
            qi_x,
            retiring
        )
        active_group = cls.update_contributions(active_group, qi_x)
        return(active_group)

    @staticmethod
    def update_contributions(active_group=active_group,
                             qi_x=qi_x):
        active_group = InvalidityContributionCalculator.update_last_invalidity_contribution(
            active_group,
            qi_x,
            invalidity_alpha
        )
        active_group = IAContributionCalculator.update_group_IA(
            active_group,
            IA_alpha,
        )
        return(active_group)

    @classmethod
    def next_year_basic_update(cls,
                               active_group=active_group,
                               players_number=players_number,
                               year=0,
                               last_ID=last_ID,
                               qi_x=qi_x,
                               retiring=base_retiring):
        active_group['age'] = active_group['age'] + 1
        active_group['salary'] = (1.06) * active_group['salary']
        active_group = cls.simulate_new_players(active_group, last_ID, year)
        active_group = add_pvfe_column(active_group)
        active_group = add_qx_column(active_group, retiring)
        return(active_group)

    @staticmethod
    def simulate_new_players(active_group, last_ID, year=0):
        columns = ['id', 'age', 'IA', 'salary', 'IA_contribution', 'invalidity_contribution', 'pvfe', 'qx']
        new_players_len = players_number - len(active_group)
        index = range(0, new_players_len)
        new_players = pd.DataFrame(index=index, columns=columns)
        new_players['id'] = range(last_ID + 1, last_ID + 1 + new_players_len)
        new_players['age'] = new_players_len * [22]
        new_players['salary'] = loc * (1 + float(sg)) ** year + np.random.gamma(shape, scale, new_players_len)
        new_players['IA'] = new_players_len * [0]
        return(active_group.append(new_players))

