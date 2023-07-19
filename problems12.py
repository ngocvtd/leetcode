import pyomo.environ as pyo

model = pyo.ConcreteModel()

months = range(1, 7)
oils = ['VEG1', 'VEG2', 'OIL1', 'OIL2', 'OIL3']

# Buying variables
model.buy = pyo.Var(oils, months, within=pyo.NonNegativeReals)

# Using variables
model.use = pyo.Var(oils, months, within=pyo.NonNegativeReals)

# Storing variables
model.store = pyo.Var(oils, months, within=pyo.NonNegativeReals)

# Product variables
model.prod = pyo.Var(months, within=pyo.NonNegativeReals)

# Objective function
model.obj = pyo.Objective(expr=sum(150 * model.prod[m] for m in months) -
                               5 * sum(model.store[o, m] for o in oils for m in months), sense=pyo.maximize)

# Constraint
model.buy_constraint = pyo.ConstraintList()
model.use_constraint = pyo.ConstraintList()
model.store_constraint = pyo.ConstraintList()
model.prod_constraint = pyo.ConstraintList()
model.hardness_constraint = pyo.ConstraintList()

# Refining constraint
for m in months:
    model.use_constraint.add(
        sum(model.use[o, m] for o in ['VEG1', 'VEG2']) <= 200
    )
    model.use_constraint.add(
        sum(model.use[o, m] for o in ['OIL1', 'OIL2', 'OIL3']) <= 250
    )

# Storage linking constraint
for m in months:
    for o in oils:
        model.store_constraint.add(model.store[o, m] <= 1000)
        if m > 1:
            model.store_constraint.add(model.store[o, m-1] + model.buy[o, m] == model.use[o, m] + model.store[o, m])
        else:
            model.store_constraint.add(model.store[o, m] == 500)

# hardness constraint
hardness_value = {
    'VEG1': 8.8,
    'VEG2': 6.1,
    'OIL1': 2.0,
    'OIL2': 4.2,
    'OIL3': 5.0
}

for m in months:
    model.hardness_constraint.add(
        sum(hardness_value[o] * (model.use[o, m] + model.store[o, m]) for o in oils) >= 3 * model.prod[m]
    )
    model.hardness_constraint.add(
        sum(hardness_value[o] * (model.use[o, m] + model.store[o, m]) for o in oils) <= 6 * model.prod[m]
    )

solver = pyo.SolverFactory('cplex')
solver.solve(model)

print("Buy variables:")
for m in months:
    for o in oils:
        print(f"buy[{o}, {m}] = {model.buy[o, m].value}")

print("\nUse variables:")
for m in months:
    for o in oils:
        print(f"use[{o}, {m}] = {model.use[o, m].value}")

print("\nStore variables:")
for m in months:
    for o in oils:
        print(f"store[{o}, {m}] = {model.store[o, m].value}")

print("\nProduct variables:")
for m in months:
    print(f"prod[{m}] = {model.prod[m].value}")

print("\nObjective Value:")

print("Obj Value = ", model.obj)
