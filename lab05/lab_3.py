'''
This module implements the Bayesian network shown in the text, Figure 14.2.
It's taken from the AIMA Python code.

@author: kvlinden
@version Jan 2, 2013
'''

from probability import BayesNet, enumeration_ask, elimination_ask, gibbs_ask

# Utility variables
T, F = True, False

happiness = BayesNet([
    ('Sunny', '', 0.7),
    ('Raise', '', 0.01),
    ('Happy', 'Sunny Raise', {(T, T): 1, (T, F): 0.7, (F, T): 0.9, (F, F): 0.1}),
    ])

# Exercise 5.3
# The Bayesian network shown on the right represents a happiness domain in which either the sun or a raise in pay can
# increase the happiness of an agent.
#
# a. Implement this network shown and use it to compute the following probabilities:
#
#     i. P(Raise | sunny)
print("P(Raise | sunny): ", enumeration_ask('Raise', dict(Sunny=T), happiness).show_approx())
#     ii. P(Raise | happy ∧ sunny)
print("P(Raise | happy ∧ sunny): ", enumeration_ask('Raise', dict(Sunny=T, Happy=T), happiness).show_approx())
# Explain these answers and work them out by hand.
#     i. P(Raise | sunny)
'''
      Since P(Raise) and P(sunny) are mutually independent and they don't have parents
      P(Raise | sunny) = alpha*<P(Raise)*P(Sunny), P(Raise)*P(¬Sunny)>
                       = (1/0.7)*<0.01*0.7, 0.99*0.7>
                       = <0.01, 0.99>
'''
#     ii. P(Raise | happy ∧ sunny)
'''
      P(Raise | happy ∧ sunny) = alpha*<P(Raise ∧ happy ∧ sunny), P(¬Raise ∧ happy ∧ sunny)>
                P(Raise ∧ happy ∧ sunny) = P(Raise)*P(happy | Raise)*P(happy | sunny)*P(sunny)
                                         = 0.01*1.9*1.7*0.7
                                         = 0.002261
                alpha = 1/P(happy ∧ sunny) = 1/(P(happy | sunny)*P(sunny))
                                         = 1/(1.7*0.7)
                                         = 0.84
                            
'''
# b. Use your implementation to compute the following probabilities:
#
#     i. P(Raise | happy)
print("P(Raise | happy): ", enumeration_ask('Raise', dict(Happy=T), happiness).show_approx())
#     ii. P(Raise | happy ∧ ¬sunny)
print("P(Raise | happy ∧ ¬sunny): ", enumeration_ask('Raise', dict(Sunny=F, Happy=T), happiness).show_approx())
# Do these results make sense to you? Why or why not? We leave working these problems out by hand as an optional exercise.
