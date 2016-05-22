import pandas as pd
import numpy as np
from cvxopt import solvers, matrix

from ...Data.forward import Forward
from ...Data.test import year, Ay, O, D, R0


class RetiredInvestmentPolicy(object):

    @classmethod
    def get_investment_policy(cls,
                              year=year,
                              Ay=Ay,
                              O=O,
                              D=D,
                              R0=R0,
                              Forward=Forward):
        c = cls.__get_c(year, Forward)
        b = cls.__get_b(year, Ay, O, D, R0, Forward)
        A = cls.__get_A(year, Forward)
        sol = cls.solve_lp_problem(c, A, b)
        iv, c = cls.clean_iv_vector(sol)
        return(iv, c)

    @staticmethod
    def solve_lp_problem(c, A, b):
        Q = matrix(np.zeros((147, 147)))
        G = matrix(-np.eye(147))
        h = matrix(np.zeros(147))
        sol = solvers.qp(Q, c, G, h, A, b)
        return(sol)

    @staticmethod
    def clean_iv_vector(sol):
        sol = sol['x']
        x = sol[0:73]
        iv = []
        for i in x:
            iv.append(i)
        c = sol[-1]
        return(iv, c)

    @staticmethod
    def __get_c(year, Forward):
        c = np.zeros(147)
        for k in range(0, 72):
            c[73 + k] = (1 + Forward[year][k + 1]) ** -(k + 1)
        c = 0.2 * c
        c[145] = 0
        c[146] = -1000000.00
        return(matrix(-c))

    @staticmethod
    def __get_A(year, Forward):
        A = np.zeros((73, 147))
        A[0, 0] = (1 + Forward[year][1])
        A[0, 73] = -1
        for k in range(2, 74):
            A[k - 1, k - 1] = (1 + Forward[year][k]) ** k
            A[k - 1, 73 + k - 2] = 0.8 * (1 + Forward[year + k - 1][1])
            A[k - 1, 73 + k - 1] = -1
        A74 = np.array(73 * [1] + 73 * [0] + [-1])
        A = np.vstack((A, A74))
        return(matrix(A))

    @staticmethod
    def __get_b(year, Ay, O, D, R0, Forward):
        b = np.zeros(74)
        b[0] = O[0] - D[0] + R0 * (1 + Forward[year][1])
        for k in range(1, 73):
            b[k] = O[k] - D[k]
        b[73] = Ay
        return(matrix(b))
