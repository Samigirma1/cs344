"""
This module implements local search on a simple sine function variant.
The function is a linear function  with a single, discontinuous max value
(see the abs function variant in graphs.py).

@author: kvlinden
@version 6feb2013
"""
from search import Problem, hill_climbing, simulated_annealing, \
    exp_schedule, genetic_search
from random import randrange
import math


class SineVariant(Problem):
    """
    State: x value for the abs function variant f(x)
    Move: a new x value delta steps from the current x (in both directions)
    """

    def __init__(self, initial, maximum=30.0, delta=0.001):
        self.initial = initial
        self.maxX = maximum
        self.delta = delta

    def actions(self, state):
        return [state + self.delta, state - self.delta]

    def result(self, stateIgnored, x):
        return x

    def value(self, x):
        return math.fabs(x * math.sin(x))
        # if x > maximum:
        #     return 0
        # else:
        #     return math.fabs(x * math.sin(x))


'''
The function professor wrote for the searches
'''

def profsFunc(max=30, debug = True):
    # Formulate a problem with a 2D hill function and a single maximum value.
    maximum = max
    initial = randrange(0, maximum)
    p = SineVariant(initial, maximum, delta=1)

    # Solve the problem using hill-climbing.
    hill_solution = hill_climbing(p)

    # Solve the problem using simulated annealing.
    annealing_solution = simulated_annealing(
        p,
        exp_schedule(k=20, lam=0.005, limit=1000)
    )

    if debug:
        print('Initial                      x: ' + str(p.initial)
              + '\t\tvalue: ' + str(p.value(initial))
              )

        print('Hill-climbing solution       x: ' + str(hill_solution)
              + '\tvalue: ' + str(p.value(hill_solution))
              )

        print('Simulated annealing solution x: ' + str(annealing_solution)
              + '\tvalue: ' + str(p.value(annealing_solution))
              )

    return {
        "init": [initial, p.value(initial)],
        "hill_final": [hill_solution, p.value(hill_solution)],
        "sa_final": [annealing_solution, p.value(annealing_solution)]
    }


'''
The worst r
'''


def forExercise2_3(numRestarts = 100, maxInitial = 30):
    average = {
        "init": [0, 0],
        "hill_final": [0, 0],
        "sa_final": [0, 0]
    }

    hill_max = []
    sa_max = []

    print("----------------------------- INDIVIDUAL -----------------------------")
    # do random restarts
    for i in range(numRestarts):
        print("------------------------------ RUN NO %d ------------------------------" % (i + 1))
        run = profsFunc(maxInitial)
        goal_sa_achieved = False
        goal_hill_achieved = False

        # average initial
        average["init"][0] += run["init"][0] / numRestarts
        average["init"][1] += run["init"][1] / numRestarts
        # average hill-climb final
        average["hill_final"][0] += run["hill_final"][0] / numRestarts
        average["hill_final"][1] += run["hill_final"][1] / numRestarts
        # average sa final
        average["sa_final"][0] += run["sa_final"][0] / numRestarts
        average["sa_final"][1] += run["sa_final"][1] / numRestarts

        # get max val
        if (goal_hill_achieved is False) or (goal_sa_achieved is False):

            if run["hill_final"][0] >= maxInitial:
                goal_hill_achieved = True
                hill_max = [run["hill_final"][0], run["hill_final"][1], i]
            if run["sa_final"][0] >= maxInitial:
                goal_sa_achieved = True
                sa_max = [run["sa_final"][0], run["sa_final"][1], i]

    # print average
    print("---------------------------------------------------------------------\n")
    print("------------------------------ AVERAGE ------------------------------")
    print('Initial                      average x: ' + str(average["init"][0])
          + '\t\taverage value: ' + str(average["init"][1])
          )
    print('Hill-climbing solution       average x: ' + str(average["hill_final"][0])
          + '\taverage value: ' + str(average["hill_final"][1])
          )
    print('Simulated annealing solution average x: ' + str(average["sa_final"][0])
          + '\taverage value: ' + str(average["sa_final"][1])
          )
    print("---------------------------------------------------------------------\n")

    print("----------------------- Goal Achievement Stats ----------------------")
    print('Hill-climbing solution       number of restarts: %d    x_val: %s   value: %s' % (hill_max[2],
                                                                                              str(hill_max[0]),
                                                                                              str(hill_max[1])))
    print('Simulated annealing soln     number of restarts: %d    x_val: %s   value: %s' % (sa_max[2],
                                                                                              str(sa_max[0]),
                                                                                              str(sa_max[1])))

if __name__ == '__main__':
    forExercise2_3()
