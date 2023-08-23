import pyomo.environ as pyo

departments = ['A', 'B', 'C', 'D', 'E']
cities = ["London", "Bristol", "Brighton"]

B = {
    ('A', 'Bristol'): 10, ('A', 'Brighton'): 10, ('A', 'London'): 0,
    ('B', 'Bristol'): 15, ('B', 'Brighton'): 20, ('B', 'London'): 1e-6,
    ('C', 'Bristol'): 10, ('C', 'Brighton'): 15, ('C', 'London'): 1e-6,
    ('D', 'Bristol'): 20, ('D', 'Brighton'): 15, ('D', 'London'): 1e-6,
    ('E', 'Bristol'): 5, ('E', 'Brighton'): 15, ('E', 'London'): 1e-6,
}

# quantities of communication
C = {
    ('A', 'B'): 0.0, ('A', 'C'): 1.0, ('A', 'D'): 1.5, ('A', 'E'): 0.0,
    ('B', 'C'): 1.4, ('B', 'D'): 1.2, ('B', 'E'): 0.0,
    ('C', 'D'): 0.0, ('C', 'E'): 2.0,
    ('D', 'E'): 0.7
}

# costs per unit of communication
D = {
    ("Bristol", "Bristol"): 5, ("Bristol", "Brighton"): 14, ("Bristol", "London"): 13,
    ("Brighton", "Brighton"): 5, ("Brighton", "London"): 9, ("Brighton", "Bristol"): 14,
    ("London", "London"): 10, ("London", "Bristol"): 13, ("London", "Brighton"): 9
}
model = pyo.ConcreteModel()

model.delta = pyo.Var(departments, cities, domain=pyo.Binary)

model.gamma = pyo.Var([(i, j, k, l) for i in departments for j in cities for k in departments for l in cities if i < k
                       and C.get((i, k), 0) != 0], domain=pyo.Binary)

# constraints
model.one_city = pyo.ConstraintList()
model.more_than_three = pyo.ConstraintList()
model.relate = pyo.ConstraintList()

# each department must be located in exactly one city
for i in departments:
    model.one_city.add(
        sum(model.delta[i, j] for j in cities) == 1
    )
# no city may be the location for more than three departments
for j in cities:
    model.more_than_three.add(
        sum(model.delta[i, j] for i in departments) <= 3
    )

for i, j, k, l in model.gamma:
    model.relate.add(
        model.gamma[i, j, k, l] == model.delta[i, j] * model.delta[k, l]
    )

# objective function
model.obj = pyo.Objective(
    expr=sum(C[i, k] * D[j, l] * model.gamma[i, j, k, l] for i, j, k, l in model.gamma) - sum(
        B[i, j] * model.delta[i, j] for i in departments for j in cities)
    , sense=pyo.minimize
)

solver = pyo.SolverFactory('cplex')
solver.solve(model)

# Print the optimal solution
if solver.status == pyo.SolverStatus.ok and solver.termination_condition == pyo.TerminationCondition.optimal:
    print("Optimal Solution Found:")
    for i in departments:
        for j in cities:
            if model.delta[i, j].value == 1:
                print(f"Department {i} should be located in {j}.")
else:
    print("No Optimal Solution Found.")
