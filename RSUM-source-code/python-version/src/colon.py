'''
File: colon.py
Author: Yutong Dai (rothdyt@gmail.com)
File Created: 2019-07-24 16:39
Last Modified: 2019-07-24 16:40
--------------------------------------------
Description:
'''
import os
import numpy as np
from sklearn.datasets import load_svmlight_file
from apcg import APCG
from rcsum import RCSUM
from csum import CSUM
from cgd import CGD
filename = os.path.basename(__file__).split('.')[0]
print(filename)
data = load_svmlight_file("../db/colon-cancer.bz2")
X, y = data[0].toarray(), data[1].reshape(-1, 1)
y[y == 1.000000] = 1
y[y == -1.000000] = 0
X = (X - np.mean(X, axis=0)) / np.std(X, axis=0)
print("Finishing Loading Data")
basedir = "../db/logs/{}".format(filename)
if not os.path.exists(basedir):
    os.makedirs(basedir)
    print("{} has been created!".format(basedir))

myLambdas = [1e-1, 1e-2, 1e-3, 1e-4, 1e-5, 1e-6]
for myLambda in myLambdas:
    print(myLambda)
    print("rcsum...")
    rcsum_solver = RCSUM(x=X, y=y, Lambda=myLambda,
                         logname="{}/rcsum_{}.log".format(basedir, myLambda))
    beta, fval_seq, running_time, iteration, epoch = rcsum_solver.solve(
        checkpoint_path="{}/rcsum_{}.pkl".format(basedir, myLambda))
    print(running_time)

    print("apcg...")
    apcg_solver = APCG(x=X, y=y, Lambda=myLambda,
                       logname="{}/apcg_{}.log".format(basedir, myLambda))
    beta, fval_seq, running_time, iteration, epoch = apcg_solver.solve(
        checkpoint_path="{}/apcg_{}.pkl".format(basedir, myLambda))
    print(running_time)

    print("csum...")
    csum_solver = CSUM(x=X, y=y, Lambda=myLambda,
                       logname="{}/csum_{}.log".format(basedir, myLambda))
    beta, fval_seq, running_time, iteration, epoch = csum_solver.solve(
        checkpoint_path="{}/csum_{}.pkl".format(basedir, myLambda))
    print(running_time)

    print("cgd...")
    cgd_solver = CGD(x=X, y=y, Lambda=myLambda,
                     logname="{}/cgd_{}.log".format(basedir, myLambda))
    beta, fval_seq, running_time, iteration, epoch = cgd_solver.solve(
        checkpoint_path="{}/cgd_{}.pkl".format(basedir, myLambda))
    print(running_time)
