import pyomo.environ as pyo

types = [1, 2, 3]
periods = [1, 2, 3, 4, 5]

min_level = {
    1: 850,
    2: 1250,
    3: 1500
}

max_level = {
    1: 2000,
    2: 1750,
    3: 4000
}

cost_min = {
    1: 1000,
    2: 2600,
    3: 3000
}

cost_mw = {
    1: 2,
    2: 1.30,
    3: 3
}

cost_start = {
    1: 2000,
    2: 1000,
    3: 500
}

load_demand = {
    1: 15000,
    2: 30000,
    3: 25000,
    4: 40000,
    5: 27000
}

num_generators_type1 = 12
num_generators_type2 = 10
num_generators_type3 = 5

model = pyo.ConcreteModel()

model.n = pyo.Var(types, periods, within=pyo.NonNegativeIntegers, bounds=lambda model, i, j: (
    0, num_generators_type1 if i == 1 else (num_generators_type2 if i == 2 else num_generators_type3)))
model.s = pyo.Var(types, periods, within=pyo.NonNegativeIntegers, bounds=lambda model, i, j: (
    0, num_generators_type1 if i == 1 else (num_generators_type2 if i == 2 else num_generators_type3)))
model.x = pyo.Var(types, periods, within=pyo.NonNegativeReals)

model.demand_constraint = pyo.ConstraintList()
model.output_limit_constraint = pyo.ConstraintList()
model.reserve_constraint = pyo.ConstraintList()
model.start_up_constraint = pyo.ConstraintList()

for j in periods:
    # demand constraint
    model.demand_constraint.add(sum(model.x[i, j] for i in types) >= load_demand[j])

    # reserve constraint
    model.reserve_constraint.add(sum(max_level[i] * model.n[i, j] for i in types) >= 1.15 * load_demand[j])

    for i in types:
        # output limit constraint
        model.output_limit_constraint.add(model.x[i, j] >= min_level[i] * model.n[i, j])
        model.output_limit_constraint.add(model.x[i, j] <= max_level[i] * model.n[i, j])

        # start up constraint
        #model.start_up_constraint.add(model.s[i, j] >= model.n[i, j] - model.n[i, j-1])

for i in types:
    for j in periods:
        if j > 1:
            model.start_up_constraint.add(model.s[i, j] >= model.n[i, j] - model.n[i, j - 1])

# cost function
def cost_function(model):
    total_cost = 0
    for i in types:
        for j in periods:
            total_cost_mw = cost_mw[i] * (model.x[i, j] - min_level[i] * model.n[i, j])
            total_cost_min = cost_min[i] * model.n[i, j]
            total_cost_started = cost_start[i] * model.s[i, j]
            total_cost += total_cost_started + total_cost_min + total_cost_mw
    return total_cost


model.obj = pyo.Objective(rule=cost_function, sense=pyo.minimize)

# Solve the model
solver = pyo.SolverFactory('cplex')
results = solver.solve(model, tee=True)

# Print the results
if results.solver.termination_condition == pyo.TerminationCondition.optimal:
    print("Optimal solution found!")
    print("Total Cost:", model.obj())
    for i in types:
        for j in periods:
            print(f"Number of generators of type {i} working in period {j}: {model.n[i, j].value}")
            print(f"Number of generators of type {i} started up in period {j}: {model.s[i, j].value}")
            print(f"Total output rate from generators of type {i} in period {j}: {model.x[i, j].value}")
else:
    print("Solver did not find an optimal solution.")
