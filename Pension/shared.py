import numpy as np
from .Data.pvfe import base_pvfe
from .Data.survival_probabilities import base_tPx


def add_pvfe_column(group, pvfe=base_pvfe):
    group['pvfe'] = group['age'].apply(lambda x: get_pvfe_for_specific_age(x, pvfe))
    return(group)


def get_pvfe_for_specific_age(age, pvfe):
    return(pvfe[age])


def add_qx_column(group, qx_dict):
    group['qx'] = group['age'].apply(lambda x: get_qx_for_specific_age(x, qx_dict))
    return(group)


def get_qx_for_specific_age(age, qx_dict):
    return(float(qx_dict[str(int(age))]))


def add_tPx_column(group, tPx_dict=base_tPx):
    group['tPx'] = group['age'].apply(lambda x: get_tPx_for_specific_age(x, tPx_dict))
    return(group)


def get_tPx_for_specific_age(age, tPx_dict):
    return(np.array(tPx_dict[age]))
