import pyomo.environ as pyo

factories = ["Liverpool", "Brighton"]
depots = ["Newcastle", "Birmingham", "London", "Exeter"]
customers = ["C1", "C2", "C3", "C4", "C5", "C6"]

# cost from factories to depots
factories_to_depots_cost = {
    ("Liverpool", "Newcastle"): 0.5, ("Liverpool", "Birmingham"): 0.5, ("Liverpool", "London"): 1.0,
    ("Liverpool", "Exeter"): 0.2,
    ("Brighton", "Birmingham"): 0.3, ("Brighton", "London"): 0.5, ("Brighton", "Exeter"): 0.2,
    ("Brighton", "Newcastle"): 1e6
}

# cost from depots to customers
depots_to_customers_cost = {
    ("Newcastle", "C2"): 1.5, ("Newcastle", "C3"): 0.5, ("Newcastle", "C4"): 1.5, ("Newcastle", "C6"): 1.0,
    ("Newcastle", "C1"): 1e6, ("Newcastle", "C5"): 1e6,
    ("Birmingham", "C1"): 1.0, ("Birmingham", "C2"): 0.5, ("Birmingham", "C3"): 0.5, ("Birmingham", "C4"): 1.0,
    ("Birmingham", "C6"): 1e6, ("Birmingham", "C5"): 0.5,
    ("London", "C2"): 1.5, ("London", "C3"): 2.0, ("London", "C5"): 0.5, ("London", "C6"): 1.5,
    ("London", "C1"): 1e6, ("London", "C4"): 1e6,
    ("Exeter", "C3"): 0.2, ("Exeter", "C4"): 1.5, ("Exeter", "C5"): 0.5, ("Exeter", "C6"): 1.5,
    ("Exeter", "C1"): 1e6, ("Exeter", "C2"): 1e6
}

# factory capacities
factory_capacities = {
    "Liverpool": 150000, "Brighton": 200000
}

# depot capacities
depot_capacities = {
    "Newcastle": 70000, "Birmingham": 50000, "London": 100000, "Exeter": 40000
}

# customer requirements
customer_requirements = {
    "C1": 50000, "C2": 10000, "C3": 40000, "C4": 35000, "C5": 60000, "C6": 20000
}

model = pyo.ConcreteModel()
model.F = pyo.Set(initialize=factories)
model.D = pyo.Set(initialize=depots)
model.C = pyo.Set(initialize=customers)

model.factory_to_depot_cost = pyo.Param(model.F, model.D, initialize=factories_to_depots_cost)
model.depot_to_customer_cost = pyo.Param(model.D, model.C, initialize=depots_to_customers_cost)
model.factory_capacity = pyo.Param(model.F, initialize=factory_capacities)
model.depot_capacity = pyo.Param(model.D, initialize=depot_capacities)
model.customer_requirement = pyo.Param(model.C, initialize=customer_requirements)

model.x = pyo.Var(model.F, model.D, domain=pyo.NonNegativeReals)
model.y = pyo.Var(model.F, model.C, domain=pyo.NonNegativeReals)
model.z = pyo.Var(model.D, model.C, domain=pyo.NonNegativeReals)


def objective_function(model):
    return (
            sum(model.factory_to_depot_cost[f, d] * model.x[f, d] for f in model.F for d in model.D) +
            sum(model.depot_to_customer_cost[d, c] * model.z[d, c] for d in model.D for c in model.C) +
            sum(model.customer_requirement[c] * model.y[f, c] for f in model.F for c in model.C)
    )


model.objective = pyo.Objective(rule=objective_function, sense=pyo.minimize)


# factory capacities
def factory_capacity_constraint(model, f):
    return sum(model.x[f, d] for d in model.D) + sum(model.y[f, c] for c in model.C) <= model.factory_capacity[f]


model.factory_capacity_constraint = pyo.Constraint(model.F, rule=factory_capacity_constraint)


# quantity into depots
def quantity_into_depots_constraint(model, d):
    return sum(model.x[f, d] for f in model.F) <= model.depot_capacity[d]


model.quantity_into_depots_constraint = pyo.Constraint(model.D, rule=quantity_into_depots_constraint)


# quantity out of depots
def quantity_out_of_depots(model, d):
    return sum(model.z[d, c] for c in model.C) == sum(model.x[f, d] for f in model.F)


model.quantity_out_of_depots = pyo.Constraint(model.D, rule=quantity_out_of_depots)


# customer requirements
def customer_requirements(model, c):
    return sum(model.y[f, c] for f in model.F) + sum(model.z[d, c] for d in model.D) == model.customer_requirement[c]


model.customer_requirements = pyo.Constraint(model.C, rule=customer_requirements)

model.customer_requirements = pyo.Constraint(model.C, rule=customer_requirements)

solver = pyo.SolverFactory('cplex')
results = solver.solve(model)


# Print the results
if results.solver.termination_condition == pyo.TerminationCondition.optimal:
    print("Optimal Solution Found")
    print("Objective Value:", pyo.value(model.objective))
    for f in model.F:
        for d in model.D:
            if pyo.value(model.x[f, d]) > 0:
                print(f"{f} -> {d}: {pyo.value(model.x[f, d])} tons")
    for f in model.F:
        for c in model.C:
            if pyo.value(model.y[f, c]) > 0:
                print(f"{f} -> {c}: {pyo.value(model.y[f, c])} tons")
    for d in model.D:
        for c in model.C:
            if pyo.value(model.z[d, c]) > 0:
                print(f"{d} -> {c}: {pyo.value(model.z[d, c])} tons")
else:
    print("No optimal solution found.")
