'''
This module implements the Bayesian network shown in the text, Figure 14.2.
It's taken from the AIMA Python code.

@author: kvlinden
@version Jan 2, 2013
'''

from probability import BayesNet, enumeration_ask, elimination_ask, gibbs_ask

# Utility variables
T, F = True, False

# From AIMA code (probability.py) - Fig. 14.2 - burglary example
cancerTest = BayesNet([
    ('Cancer', '', 0.01),
    ('Test1', 'Cancer', {T: 0.9, F: 0.2}),
    ('Test2', 'Cancer', {T: 0.9, F: 0.2})
    ])

# Exercise 5.2
# Pull network.py and add enumeration_ask computations for the following examples:
#
# a. P(Cancer | positive results on both tests)
print("\n P(Cancer | T1 ∧ T2): ",
      enumeration_ask('Cancer', dict(Test1=T, Test2=T), cancerTest).show_approx())

# b. P(Cancer | a positive result on test 1, but a negative result on test 2)
print("\n P(Cancer | T1 ∧ ¬T2): ",
      enumeration_ask('Cancer', dict(Test1=T, Test2=F), cancerTest).show_approx())

'''
Do the results make sense? How much effect does one failed test have on the probability of having cancer?



Explain your answers and work them out by hand.

P(Cancer | T1 ∧ T2) = alpha*P(Cancer, T1, T2)
                         P(Cancer, T1, T2) = P(Cancer)*P(Cancer|T1)*P(Cancer|T2)
                             P(Cancer | T1) = P(T1 | Cancer)*P(Cancer) / P(T1)
                                 P(T1) = P(T1 and Cancer) + P(T1 and ¬Cancer)
                                       = P(T1 | Cancer)*P(Cancer) + P(T1 | ¬Cancer)*P(¬Cancer)
                                       = 0.9 * 0.01 + 0.2*0.99
                                       = 0.207
                             P(Cancer | T1) = 0.9*0.01 / 0.207
                                            = 0.0435
                             P(Cancer | T2) = P(Cancer | T1) - because the conditional probabilities of T1 and T2 are the 
                                                               same
                         P(Cancer, T1, T2) = 0.01*0.0435*0.0435 = 0.000189225
                         alpha = 1/P(T1, T2) = 1/(P(T1)*P(T2))
                                           = 1/(0.207*0.207) = 23.34
P(Cancer | T1 and T2) = 23.34*0.00189225 =            
                         

'''