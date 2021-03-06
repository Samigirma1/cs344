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

ANSWER: Failing to test positive on either of the tests will dramatically decrease the likelihood of having cancer. This
        because the conditional probability of getting a false negative is low (0.1).

Explain your answers and work them out by hand.

P(Cancer | T1 ∧ T2) = alpha*<P(Cancer, T1, T2), P(¬Cancer, T1, T2)>
                    = alpha*<P(Cancer)*P(T1|Cancer)*P(T2|Cancer), P(¬Cancer)*P(T1|¬Cancer)*P(T2|¬Cancer)>
                    = alpha*<0.01*0.9*0.9, 0.99*0.2*0.2>
                    = 1/(0.0081 + 0.0396)<0.0081, 0.0396>
                    = <0.1698, 0.8301>          
                         
P(Cancer | T1 ∧ ¬T2) = alpha*<P(Cancer, T1, ¬T2), P(¬Cancer, T1, ¬T2)>
                    = alpha*<P(Cancer)*P(T1|Cancer)*P(¬T2|Cancer), P(¬Cancer)*P(T1|¬Cancer)*P(¬T2|¬Cancer)>
                    = alpha*<0.01*0.9*0.1, 0.99*0.2*0.8>
                    = 1/(0.0009 + 0.1584)<0.0009, 0.1584>
                    = <0.00565, 0.99435>
'''
cancerTest = BayesNet([
    ('Cancer', '', 0.01),
    ('Test1', 'Cancer', {T: 0.9, F: 0.2}),
    ('Test2', 'Cancer', {T: 0.9, F: 0.2})
    ])