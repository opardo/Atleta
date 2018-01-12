# Atleta

## Overview

Python project for the Práctica Actuarial y Marco Institucional (Standards of Actuarial Practice) class, offered by the Mexico Autonomous Institute of Technology (ITAM) in the Spring 2016 semester.

It considers a hypothetical retirement plan for NFL players. The code performs multiple simulations to measure the uncertainty obtained after stressing variables that we know are volatile. These simulations will allow our team to estimate financial projections in the short, medium and long term.

## Requirements

python: 2.7.14,
pandas: 0.18.1,
numpy: 1.14.0,
cvxopt: 1.1.8

## Code

The code is organized in different classes. To perform the simulations you have to run the following code in a Python console:
```
from Pension.Simulations.simulate import *
Simulate.simulate_one_setting('mortality_stressed_simulated_table.csv')
```
