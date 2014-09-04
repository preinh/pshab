from __future__ import division
  
from openopt import MINLP
from openopt import MINLP
from numpy import *

N = 150
K = 50
#objective function:
f = lambda x: ((x-5.45)**2).sum()

#optional: 1st derivatives
df = lambda x: 2*(x-5.45)

# start point
x0 = 8*cos(arange(N))
p = MINLP(f, x0, df=df, maxIter = 1e3)

# optional: set some box constraints lb <= x <= ub
p.lb = [-6.5]*N
p.ub = [6.5]*N
# see help(NLP) for handling of other constraints: 
# Ax<=b, Aeq x = beq, c(x) <= 0, h(x) = 0
# see also /examples/nlp_1.py

# required tolerance for smooth constraints, default 1e-6
p.contol = 1.1e-6

p.name = 'minlp_1'
nlpSolver = 'ipopt'

# coords of discrete variables and sets of allowed values
p.discreteVars = {7:range(3, 10), 8:range(3, 10), 9:[2, 3.1, 9]}

# required tolerance for discrete variables, default 10^-5
p.discrtol = 1.1e-5

#optional: check derivatives, you could use p.checkdc(), p.checkdh() for constraints
#p.checkdf()

# optional: maxTime, maxCPUTime
# p.maxTime = 15
# p.maxCPUTime = 15

r = p.solve('branb', nlpSolver=nlpSolver, plot = False)
# optim point and value are r.xf and r.ff,
# see http://openopt.org/OOFrameworkDoc#Result_structure for more details
# 
#  
# import coopr.pyomo as po
#  
# model = po.AbstractModel()
#   
# # model.r_min = po.Param(within=po.NonNegativeReals)
# # model.a = po.Param(within=po.NonNegativeIntegers)
# # model.k = po.Param(within=po.NonNegativeIntegers)
# # 
# # model.I = po.RangeSet(1, model.m)
# # model.J = po.RangeSet(1, model.n)
#   
# from openopt import MINLP
