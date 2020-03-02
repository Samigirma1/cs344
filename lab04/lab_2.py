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
P = JointProbDist(['Toothache', 'Cavity', 'Catch', 'Rain'])
T, F = True, False

# P(Rain) = 0.15; P(not(Rain)) = 0.85
P[T, T, T, T] = 0.0162
P[T, T, T, F] = 0.0918
P[T, T, F, T] = 0.0018
P[T, T, F, F] = 0.0102
P[T, F, T, T] = 0.0024
P[T, F, T, F] = 0.0136
P[T, F, F, T] = 0.0096
P[T, F, F, F] = 0.0544
P[F, T, T, T] = 0.0108
P[F, T, T, F] = 0.0612
P[F, T, F, T] = 0.0012
P[F, T, F, F] = 0.0068
P[F, F, T, T] = 0.0216
P[F, F, T, F] = 0.1224
P[F, F, F, T] = 0.0864
P[F, F, F, F] = 0.4896

# Compute P(Cavity|Toothache=T)  (see the text, page 493).
# PC = enumerate_joint_ask('Cavity', {'Toothache': T}, P)
# print(PC.show_approx())

'''
Excercise 4.2
If you have time, do the following exercises based on your code from the previous exercise for extra credit.

a. Modify the domain to include a new random variable Rain, which takes on values rain or not rain, and then do the 
   following:

    i.   How many entries does your full joint probability distribution contain now?
        ANSWER: 16
    ii.  Do the probabilities sum up to 1.0? Should they? Explain why or why not.
        ANSWER: 
            Reason 1 - The probability of all events in a sample space should add to 1.
            
            Proof?  If the events are independent, then P(A ∩ B) = P(A)*P(B). Since the occurrence of rain is 
              independent of toothaches, cavity, and catching cold,
                
                let sum(P(ToothAche and Cavity and Catch)) be the sum of probabilities before adding the rain variable,
                which is equal to 1
                
                sum(P(ToothAche and Cavity and Catch and Rain)) = sum(P(ToothAche and Cavity and Catch) * P(Rain))
                sum(P(ToothAche and Cavity and Catch and ¬Rain)) = sum(P(ToothAche and Cavity and Catch) * P(¬Rain))
                                                            = sum(P(ToothAche and Cavity and Catch) * (1 - P(Rain)))
                So ->  sum(P(ToothAche and Cavity and Catch) * P(Rain)) + sum(P(ToothAche and Cavity and Catch) * P(¬Rain))
                       sum(P(ToothAche and Cavity and Catch) * P(Rain) + P(ToothAche and Cavity and Catch) * (1 - P(Rain)))
                       sum(P(ToothAche and Cavity and Catch)) = 1
                       
                       
    iii. Did you think that you can use anything other than T or F values for the values for the random variables? 
         Explain why or why not.
         ANSWER:
                - An event can either occur or not-occur. So, the value of the variables should be either true or false.
                - Random variables map values in a domain to either true or false. So, use have to use either True or 
                  False.
         
    iv.  Did the probabilities you chose indicate that the value of Rain is independent of the original values?
         ANSWER:
                - Yes
b. Compute the value of P(Toothache|rain). Again, compute this value on pencil and paper, and then verify your answer by
   adding code to compute the specified value.
    ANSWER: 
        P(Toothache|Rain) = P(Toothache ∩ Rain) / P(Rain)
            P(Toothache ∩ Rain) = P(Toothache ∩ Cavity ∩ ¬Catch ∩ Rain) +
                                  P(Toothache ∩ Cavity ∩ Catch ∩ Rain) +
                                  P(Toothache ∩ ¬Cavity ∩ ¬Catch ∩ Rain) +
                                  P(Toothache ∩ ¬Cavity ∩ Catch ∩ Rain)
                                = 0.0018 + 0.0162 + 0.0096 + 0.0024
                                = 0.03
        P(Toothache|Rain) = 0.03 / 0.85 = 0.035
'''

PC = enumerate_joint_ask('Toothache', {'Rain': True}, P)
print("For exercise 2:\n", PC.show_approx())