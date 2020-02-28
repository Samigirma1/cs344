'''
This module implements a simple classroom example of probabilistic inference
over the full joint distribution specified by AIMA, Figure 13.3.
It is based on the code from AIMA probability.py.

@author: kvlinden
@version Jan 1, 2013
Completed by: Samuel Zeleke
Date: Feb 28, 2020
Lab 04
'''

from probability import JointProbDist, enumerate_joint_ask

# The Joint Probability Distribution Fig. 13.3 (from AIMA Python)
P = JointProbDist(['Toothache', 'Cavity', 'Catch'])
T, F = True, False
P[T, T, T] = 0.108; P[T, T, F] = 0.012
P[F, T, T] = 0.072; P[F, T, F] = 0.008
P[T, F, T] = 0.016; P[T, F, F] = 0.064
P[F, F, T] = 0.144; P[F, F, F] = 0.576

# Compute P(Cavity|Toothache=T)  (see the text, page 493).
# PC = enumerate_joint_ask('Cavity', {'Toothache': T}, P)
# print(PC.show_approx())

'''
EX1.b Compute the value of P(Cavity|catch):
    i.  First, compute it by hand.
        P(Cavity|Catch) = alpha*P(Cavity, Catch)
                    = alpha*(P(Cavity, Toothache, Catch) + P(Cavity, not(Toothache), Catch))
                          alpha = 0.108 + 0.016 + 0.072 + 0.144
                                = 0.34
                          P(Cavity, Toothache, Catch) = 0.108
                          P(Cavity, not(Toothache), Catch) = 0.072
                    = 0.34 * (0.108 + 0.072)
                    = 0.5294
    ii. Verify your answer (and the AIMA implementation) by adding code to compute the specified value.
'''

PC = enumerate_joint_ask('Cavity', {'Catch': T}, P)
print("For exercise 1.b.ii:\n", PC.show_approx())

'''
EX.1.c Create a new probability density function that implements the flipping of two coins and then compute the 
probability of P(Coin2|coin1=heads). Does the answer confirm what you believe to be true about the probabilities of 
flipping coins?

The result meets my expectation because the two events are independent. So, fixing the value of one coin does not 
influence of the probabilities of the other coin.
'''
P2 = JointProbDist(['Coin1', 'Coin2'])
Heads, Tails = True, False
P2[Heads, Heads] = P2[Heads, Tails] = P2[Tails, Heads] = P2[Tails, Tails] = 0.25
PC2 = enumerate_joint_ask('Coin2', {'Coin1': Heads}, P2)
print("For exercise 1.c P(Coin2 | Coin1 = Heads):\n", PC2.show_approx())

