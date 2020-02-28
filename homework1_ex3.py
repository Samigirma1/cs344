from csp import CSP, backtracking_search, mrv, \
    forward_checking, min_conflicts
import random
import timeit

def schedule_func():
    instructors = ["Schuurman", "Adams", "VanderLinden", "Bailey"]
    courses = ["cs108", "cs112", "cs212", "cs214", "cs232", "cs262", "cs300"]
    times = ["MWF 9:00 AM", "MWF 10:30 AM", "MWF 1:00 PM", "TuThur 10:30 AM", "TuThur 1:30 PM"]
    classRooms = ["SB354", "SB372"]
    variables = courses

    # generate domain
    domain = {}
    for course in courses:
        course_domain = []
        for classRoom in classRooms:
            for instructor in instructors:
                for time in times:
                    course_domain.append(
                        classRoom + "_" + instructor + "_" + time
                    )
        random.shuffle(course_domain)
        domain[course] = course_domain

    # generate neighbours
    neighbours = {}
    for variable in variables:
        variable_temp = variables[:]
        variable_temp.remove(variable)
        neighbours[variable] = variable_temp

    def schedule_constraint(var1, var1Val, var2, var2Val):
        var1_props = var1Val.split("_")
        var2_props = var2Val.split("_")

        if (  # if the two course have the same class and time
                (var1_props[0] == var2_props[0] and var1_props[2] == var2_props[2]) or
                # if  two course have the same time and prof
                (var1_props[1] == var2_props[1] and var1_props[2] == var2_props[2])):
            return False

        return True

    return CSP(variables, domain, neighbours, schedule_constraint)

solutionTimes = {}
solutions = {}
problem = schedule_func()

# 2. Solve the problem.
# There is a bug in the DFS code (even for 1-queens), so skip this one.
# solution = depth_first_graph_search(problem)
# solution = AC3(problem)
start = timeit.timeit()
solution = backtracking_search(problem) #28
solutionTimes["BtrackDefault"] = start - timeit.timeit()
solutions["BtrackDefault"] = solution

start = timeit.timeit()
solution = backtracking_search(problem, select_unassigned_variable=mrv) #50
solutionTimes["BtrackMRV"] = start - timeit.timeit()
solutions["BtrackMRV"] = solution

start = timeit.timeit()
solution = backtracking_search(problem,  inference=forward_checking)
solutionTimes["BtrackFC"] = start - timeit.timeit()
solutions["BtrackFC"] = solution

start = timeit.timeit()
solution = backtracking_search(problem, select_unassigned_variable=mrv, inference=forward_checking)
solutionTimes["BtrackMRVFC"] = start - timeit.timeit()
solutions["BtrackMRVFC"] = solution

start = timeit.timeit()
solution = min_conflicts(problem)
solutionTimes["minConf"] = start - timeit.timeit()
solutions["minConf"] = solution

# 3. Print the results.
# Handle AC3 solutions (boolean values) first, they behave differently.
# if type(solution) is bool:
#     if solution and problem.goal_test(problem.infer_assignment()):
#         print('AC3 Solution:')
#     else:
#         print('AC Failure:')
#     print(problem.curr_domains)

# Handle other solutions next.
for algorithm in solutions:
    if solutions[algorithm] is not None and problem.goal_test(solutions[algorithm]):
        print('\n%s Solution:' %(algorithm))
        for key in solution:
            temp = solutions[algorithm][key].split("_")
            print("%s is taught by %s in %s on %s" %(key, temp[1], temp[0], temp[2]))

        print("Time taken by %s: %d\n" %(algorithm, solutionTimes[algorithm]))

    else:
        print('Failed - domains: ' + str(problem.curr_domains))
        problem.display(problem.infer_assignment())
