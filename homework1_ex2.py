
from search import Problem, hill_climbing, simulated_annealing, exp_schedule
import itertools
import random
import math


class TSP(Problem):
    """An implementation of NQueens for local search. This is a complete-state
    reformulation of the partial-state AIMA-Python version.

    State representation:
        [q1, q2, ..., qn] gives the row for each of the n queens.
    Move representation:
        [column, row]: Move the queen in the given column to the given row.
    """

    def __init__(self, adj_matrix, initial_path):

        self.adj_matrix = adj_matrix
        self.numCities = len(adj_matrix)
        self.initial = initial_path

    def actions(self, state):
        """Actions move the queen in each column to any of the other,
        unfilled row spots.
        """
        return list([swaps for swaps in itertools.combinations(state, 2)])

    def result(self, state, move):
        """Makes the given move on a copy of the given state."""
        new_state = state[:]

        new_state[state.index(move[0])] = move[1]
        new_state[state.index(move[1])] = move[0]

        return new_state

    def value(self, state):
        """This method computes a value of given state based on the number of
        conflicting pairs of queens. It doesn't follow AIMA-Python's NQueens
        gradient-descent formulation; instead, it counts the number of
        non-conflicting pairs (e.g., top score: 28 for a 8-queen problem;
        worst score: 0).
        """

        # Start with the highest possible score (n combined 2)
        score = 0

        # Loop through all pairs, subtracting one for every conflicted pair.
        for i in range(self.numCities - 1):
            score -= self.adj_matrix[state[i]][state[i + 1]]

        return score


if __name__ == '__main__':

    # Set the board size.
    adj = [
        [0, 2, 3, 4],
        [2, 0, 4, 5],
        [3, 4, 0, 6],
        [4, 5, 6, 0]
    ]

    init = []

    for i in range(len(adj)):
        init.append(i)

    random.shuffle(init)
    print("Adj list:\n ")
    for i in range(len(adj)):
        print ("\tFor ", i, ": ", adj[i], "\n")

    # Initialize the board with all queens in the first row.

    print('Start:\t' + str(init))

    # Initialize the NQueens problem
    p = TSP(adj, init)
    print('Value:\t' + str(p.value(init)))

    # Solve the problem using hill climbing.
    hill_solution = hill_climbing(p)
    print('\nHill-climbing:')
    print('\tSolution:\t' + str(hill_solution))
    print('\tValue:\t\t' + str(p.value(hill_solution)))
    # print('\tGoal?\t\t' + str(p.goal_test(hill_solution)))

    # Solve the problem using simulated annealing.
    annealing_solution = \
        simulated_annealing(p, exp_schedule(k=20, lam=0.005, limit=10000))
    print('\nSimulated annealing:')
    print('\tSolution:\t' + str(annealing_solution))
    print('\tValue:\t\t' + str(p.value(annealing_solution)))
    # print('\tGoal?\t\t' + str(p.goal_test(annealing_solution)))
