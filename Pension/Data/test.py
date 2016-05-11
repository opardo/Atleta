import pandas as pd
import numpy as np

active_group = pd.DataFrame({
    'id': [1, 2, 3, 4],
    'age': [31, 37, 33, 29],
    'IA': [1000, 2000, 3000, 4000],
    'salary': [200, 400, 500, 600],
    'IA_contribution': [100, 200, 300, 400],
    'invalidity_contribution': [1, 2, 3, 4],
})

invalid_group = pd.DataFrame({
    'id': [1, 2, 3, 4],
    'age': [45, 56, 72, 32],
    'retirement_age': [32, 40, 36, 29],
    'last_salary': [200, 400, 500, 600]
})

retired_group = pd.DataFrame({
    'id': [1, 2, 3, 4],
    'age': [45, 56, 72, 32],
    'retirement_age': [32, 40, 36, 29],
    'payment': [50, 100, 125, 150],
})


