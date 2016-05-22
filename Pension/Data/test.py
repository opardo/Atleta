import pandas as pd
import numpy as np

D_IA = 3000 * np.ones(73)
D_inv = 2000 * np.ones(73)
life = 0
year = 1
last_ID = 10

active_group = pd.DataFrame({
    'id': [1, 2, 3, 4, 5, 6, 7, 8],
    'age': [31, 37, 33, 29, 37, 28, 34, 36],
    'IA': [1000, 2000, 3000, 4000, 8000, 8000, 5000, 3000],
    'salary': [200, 400, 500, 600, 600, 450, 450, 600],
    'IA_contribution': [100, 200, 300, 400, 500, 600, 700, 800],
    'invalidity_contribution': [1, 2, 3, 4, 5, 6, 7, 8],
    'pvfe': [31, 32, 33, 34, 35, 36, 37, 38],
    'qx': [0.5, 0.1, 0.5, 0.1, 0.5, 0.1, 0.5, 0.1]
})

invalid_group = pd.DataFrame({
    'id': [1, 2, 3, 4],
    'age': [45, 56, 72, 32],
    'retirement_age': [32, 40, 36, 29],
    'last_salary': [200, 400, 500, 600]
})

retired_group = pd.DataFrame({
    'id': [21, 22, 23, 24, 25, 26, 27, 28],
    'age': [45, 56, 72, 32, 45, 34, 46, 86],
    'retirement_age': [32, 40, 36, 29, 41, 30, 39, 38],
    'IA_pension': [50, 100, 125, 150, 560, 450, 320, 280],
    'invalidity_pension': [1000, 0, 0, 0, 670, 0, 0, 0],
    'pvfe': [25, 43, 35, 45, 32, 20, 19, 18],
    'qx': [0.2, 0.2, 0.2, 0.2, 0.2, 0.2, 0.2, 0.2],
    'retired_years': [13, 16, 36, 3, 4, 4, 7, 48],
    'last_salary': [200, 400, 500, 600, 800, 500, 300, 100]
})

retiring_group = pd.DataFrame({
    'id': [1, 2, 3, 4],
    'age': [31, 37, 33, 29],
    'IA': [1000, 2000, 3000, 4000],
    'salary': [200, 400, 500, 600],
    'IA_contribution': [100, 200, 300, 400],
    'invalidity_contribution': [1, 2, 3, 4],
})

# Investment Policy
year = 0
Ay = 0
O = 100 * np.ones(73)
D = 80 * np.ones(73)
R0 = 50
