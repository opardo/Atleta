import pandas as pd
import numpy as np
from cvxopt import solvers, matrix

from ...Data.forward import Forward
from ...Data.test import year, Ay, O, D, R0


class RetiredInvestmentPolicy(object):

    @classmethod
    def get_investment_policy(cls):
        return()

    @classmethod
    def get_investment_vector(cls,
                              year=year,
                              Ay=Ay,
                              O=O,
                              D=D,
                              R0=R0,
                              Forward=Forward):

        c = cls.__get_c(year, Forward)
        b = cls.__get_b(year, Ay, O, D, R0, Forward)
        A = cls.__get_A(year, Forward)
        Q = matrix(np.zeros((146, 146)))
        G = matrix(-np.eye(146))
        h = matrix(np.zeros(146))
        sol = solvers.qp(Q, c, G, h, A, b)
        x = sol['x']
        x = x[0:73]
        iv = []
        for i in x:
            iv.append(i)
        return(iv)

    @staticmethod
    def __get_c(year, Forward):
        c = np.zeros(146)
        for k in range(0, 72):
            c[73 + k] = (1 + Forward[year][k + 1]) ** -(k + 1)
        c = 0.2 * c
        c[145] = Forward[year][73]
        return(matrix(-c))

    @staticmethod
    def __get_b(year, Ay, O, D, R0, Forward):
        b = np.zeros(74)
        b[0] = O[0] - D[0] + R0 * (1 + Forward[year][1])
        for k in range(1, 73):
            b[k] = O[k] - D[k]
        b[73] = Ay
        return(matrix(b))

    @staticmethod
    def __get_A(year, Forward):
        A = np.zeros((73, 146))
        A[0, 0] = (1 + Forward[year][1])
        A[0, 73] = -1
        for k in range(2, 74):
            A[k - 1, k - 1] = (1 + Forward[year][k]) ** k
            A[k - 1, 73 + k - 2] = 0.8 * (1 + Forward[year + k - 1][1])
            A[k - 1, 73 + k - 1] = -1
        A74 = np.array(73 * [1] + 73 * [0])
        A = np.vstack((A, A74))
        return(matrix(A))
