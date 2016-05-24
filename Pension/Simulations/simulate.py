import pandas as pd
import numpy as np
import pickle

from ..Data.df_parameters import *
from ..Data.parameters import *
from ..GroupsMGMT.active_group import *
from ..GroupsMGMT.retired_group import *
from ..GroupsMGMT.retiring_group import *
from ..Reserve.Calculator.RLR import *
from ..Reserve.Calculator.RMI import *
from ..Reserve.Calculator.RMR import *
from ..Reserve.Calculator.RRCI import *
from ..Investment.Calculator.retired_policy import *

# from Pension.Simulations.simulate import *
# Simulate.simulate_one_setting('mortality_stressed_simulated_table.csv')


class Simulate(object):

    @classmethod
    def simulate_one_setting(
        cls,
        table_name,
        retiring=base_retiring,
        mortality=base_mortality,
        retiring_reasons_probabilities=base_retiring_reasons_probabilities,
        qi_x=qi_x,
    ):
        table = pd.DataFrame(index=[], columns=columns)
        for life in range(1, 501):
            print 'LIFE: ' + str(life)
            try:
                life_table = cls.simulate_one_life(
                    life,
                    retiring,
                    mortality,
                    retiring_reasons_probabilities,
                    qi_x,
                )
                table = table.append(life_table)
            except:
                pass
        table = table.to_csv(table_name)
        table['NumPartRet'] = table['NumPartMuertos'] + table['NumPartInv'] + table['NumPartVol']
        table['R0Inv*0.2'] = 0.2 * table['R0Inv']
        table['R0Ret*0.2'] = 0.2 * table['R0Ret']
        table['CSInv'] = table['CRNInv'] + table['CPInv']
        table['CSRet'] = table['CRNRet'] + table['CPRet']
        table = delta(table, 'VLR', 'DeltaVLR')
        table = delta(table, 'VMI', 'DeltaVMI')
        table = delta(table, 'VMR', 'DeltaVMR')
        table = delta(table, 'VRCI', 'DeltaVRCI')
        table = table.to_csv(table_name)

    @classmethod
    def simulate_one_life(
        cls,
        life,
        retiring,
        mortality,
        retiring_reasons_probabilities,
        qi_x,
    ):
        table = pd.DataFrame(index=[], columns=columns)
        last_ID = 0
        D_IA = None
        D_inv = None
        active_group = pickle.load(
            open("./Pension/Data/active_group.pickle", "rb")
        )
        retired_group = pickle.load(
            open("./Pension/Data/retired_group.pickle", "rb")
        )
        for year in range(0, 51):
            (
                year_table,
                active_group,
                retired_group,
                D_IA,
                D_inv,
                last_ID,
            ) = cls.simulate_one_year(
                life,
                year,
                active_group,
                retired_group,
                D_IA,
                D_inv,
                last_ID,
                retiring,
                mortality,
                retiring_reasons_probabilities,
                qi_x
            )
            table = table.append(year_table)
        return(table)

    @staticmethod
    def simulate_one_year(
        life,
        year,
        active_group,
        retired_group,
        D_IA,
        D_inv,
        last_ID,
        retiring=base_retiring,
        mortality=base_mortality,
        retiring_reasons_probabilities=base_retiring_reasons_probabilities,
        qi_x=qi_x
    ):

        table = pd.DataFrame(index=index, columns=columns)
        table['Life'] = life
        table['Year'] = year
        active_group = UpdateActiveGroup.starting_update(
            active_group,
            retiring,
            players_number,
            year,
            last_ID,
            qi_x
        )
        last_ID = max(active_group['id'])
        table['ComRend'] = UpdateActiveGroup.get_yield_commissions(active_group)
        table['AP'] = IAContributionCalculator.get_total_last_IA_contribution(
                    active_group
                )
        table['BI'] = InvalidityContributionCalculator.get_total_invalidity_contribution(
                    active_group
        )
        table['PT'] = UpdateActiveGroup.get_premium_rate(active_group)
        table['VLR'] = RLR.get_group_BEL(active_group)
        table['VRCI'] = RRCI.get_group_BEL(active_group)
        active_group = UpdateActiveGroup.update_yield_IA(active_group)
        table['VMI'] = RMI.get_group_BEL(retired_group)
        table['VMR'] = RMR.get_group_BEL(retired_group)
        retired_group = retired_group.drop(['accumulated_growth', 'todays_salary'], axis=1)
        retired_group, table['NumRetMuertos'] = MortalityRetiredGroup.simulate_mortality(
            retired_group
        )
        active_group, retiring_group = RetiringActiveGroup.simulate_retirement(active_group)
        volunteer_group, death_group, invalid_group = RetiringReason.simulate_retiring_reasons_groups(
            retiring_group,
            retiring_reasons_probabilities=base_retiring_reasons_probabilities
        )
        table['NumPartMuertos'] = len(death_group)
        table['NumPartInv'] = len(invalid_group)
        table['NumPartVol'] = len(volunteer_group)
        volunteer_group, invalid_group = CalculatePensions.calculate_invalid_and_volunteer_groups_pensions(
            volunteer_group,
            invalid_group,
            base_pvfe
        )
        table['MontoMuerte'] = death_group['IA'].sum()
        table['MontoInv'] = CalculatePensions.get_pvfe_invalid_generation(invalid_group)
        table['MontoRet'] = CalculatePensions.get_pvfe_IA_generation(volunteer_group, invalid_group)
        table['PagoPrimPensionInv'] = CalculatePensions.get_generation_this_year_invalid_pension(invalid_group)
        table['PagoPrimPensionRet'] = CalculatePensions.get_generation_this_year_IA_pension(volunteer_group, invalid_group)
        table['InDispInv'] = table['MontoInv'] - table['PagoPrimPensionInv']
        table['InDispRet'] = table['MontoRet'] - table['PagoPrimPensionRet']
        volunteer_group, invalid_group = UpdateRetiringGroup.update(
            volunteer_group,
            invalid_group,
            mortality=base_mortality
        )
        retired_group = UpdateRetiredGroup.update_past_retired(
            retired_group,
            mortality=base_mortality,
            pvfe=base_pvfe
        )
        table['PagoAntInv'] = RetiredInvestment.get_O0(retired_group, 'invalidity_pension')
        table['PagoAntRet'] = RetiredInvestment.get_O0(retired_group, 'IA_pension')
        retired_group = UpdateRetiredGroup.add_new_retired(retired_group, volunteer_group, invalid_group)

        obligations_IA = RetiredInvestment.get_obligations_vector(
            retired_group,
            'IA_pension',
            tPx_dict=base_tPx
        )
        obligations_inv = RetiredInvestment.get_obligations_vector(
            retired_group,
            'invalidity_pension',
            tPx_dict=base_tPx
        )
        retired_group = retired_group.drop(['accumulated_growth', 'tPx'], axis=1)
        if D_IA is None:
            D_IA = np.zeros(73)
        if D_inv is None:
            D_inv = np.zeros(73)
        table['InVencInv'] = float(D_inv[0])
        table['InVencRet'] = float(D_IA[0])
        table['CRNInv'], table['R0Inv'] = RetiredInvestment.get_CRN_and_R0(float(table['InVencInv']), float(table['PagoAntInv']))
        table['CRNRet'], table['R0Ret'] = RetiredInvestment.get_CRN_and_R0(float(table['InVencRet']), float(table['PagoAntRet']))
        IV_IA, table['CPRet'] = RetiredInvestmentPolicy.get_investment_policy(
            year=float(table['Year']),
            Ay=table['InDispRet'],
            O=obligations_IA,
            D=D_IA,
            R0=float(table['R0Ret']),
        )
        IV_inv, table['CPInv'] = RetiredInvestmentPolicy.get_investment_policy(
            year=float(table['Year']),
            Ay=table['InDispInv'],
            O=obligations_inv,
            D=D_inv,
            R0=float(table['R0Inv']),
        )
        D_inv = RetiredInvestment.update_D_vector(D_inv, IV_inv, float(table['Year']))
        D_IA = RetiredInvestment.update_D_vector(D_IA, IV_IA, float(table['Year']))

        table.fillna(0, inplace=True)

        return(
            table,
            active_group,
            retired_group,
            D_IA,
            D_inv,
            last_ID,
        )
