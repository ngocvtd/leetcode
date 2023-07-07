from pyomo.opt import (SolverFactory, TerminationCondition)
from Soduku.SodokuModel import (create_sodoku_model, print_solution, add_integer_cut)

# define the board

board = [(1,1,9), (1,8,1),
         (2,1,3), (2,4,9), (2,8,8), (2,9,6),
         (3,3,2), (3,6,3),
         (4,2,7), (4,5,5),
         (5,1,2), (5,4,8), (5,8,3), (5,9,9),
         (6,7,4),
         (7,3,5), (7,5,8), (7,8,6), (7,9,4),
         (8,4,4), (8,7,2),
         (9,1,6), (9,7,1)]

model = create_sodoku_model(board)

solution_count = 0
while 1:
    with SolverFactory('cplex') as opt:
        results = opt.solve(model)
        if results.solver.termination_condition != TerminationCondition.optimal:
            print("All board solutions have been found")
            break
    solution_count +=1

    add_integer_cut(model)
    print("Solution #%d" % (solution_count))
    print_solution(model)