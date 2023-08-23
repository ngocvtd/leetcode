import pyomo.environ as pyo

industries = ['C', 'S', 'T']  # coal, steel, transport
years = [1, 2, 3, 4, 5]
extra_years = [2, 3, 4, 5, 6]

initial_capacity = {'C': 300, 'S': 350, 'T': 280}
initial_stocks = {'C': 150, 'S': 80, 'T': 100}
exogenous_demand = {'C': 60, 'S': 60, 'T': 30}

# from table 12.1 and 12.2
c_coefficients = {
    ('C', 'C'): 0.1, ('C', 'S'): 0.5, ('C', 'T'): 0.4,
    ('S', 'C'): 0.1, ('S', 'S'): 0.1, ('S', 'T'): 0.2,
    ('T', 'C'): 0.2, ('T', 'S'): 0.1, ('T', 'T'): 0.2,
    ('M', 'C'): 0.6, ('M', 'S'): 0.3, ('M', 'T'): 0.2,
}

d_coefficients = {
    ('C', 'C'): 0.0, ('C', 'S'): 0.7, ('C', 'T'): 0.9,
    ('S', 'C'): 0.1, ('S', 'S'): 0.1, ('S', 'T'): 0.2,
    ('T', 'C'): 0.2, ('T', 'S'): 0.1, ('T', 'T'): 0.2,
    ('M', 'C'): 0.4, ('M', 'S'): 0.2, ('M', 'T'): 0.1,
}
# create model
model = pyo.ConcreteModel()

# total output of industry in year
model.x = pyo.Var(industries, years, within=pyo.NonNegativeReals)

# stock level
model.s = pyo.Var(industries, years, within=pyo.NonNegativeReals)

# extra productive
model.y = pyo.Var(industries, years, within=pyo.NonNegativeReals)


# Maximizing total productive capacity at the end of five years
def objective_rule(model):
    return sum(model.y[i, l] for i in industries for l in range(1, 6))


model.objective = pyo.Objective(rule=objective_rule, sense=pyo.maximize)


# constraint total input in each year
def total_output_rule(model, i, t):
    return sum(model.x[j, t] * c_coefficients[i, j] for j in range(1, 4)) + sum(
        model.y[j, t + 2] * d_coefficients[i, j] for j in range(1, 4)) \
           + model.s[i, t] - model.s[i, t + 1] - exogenous_demand[i]


model.total_output_constraints = pyo.Constraint(industries, years, rule=total_output_rule)


# constraint manpower
def manpower_constraint_rule(model, t):
    return 0.6 * model.x['C', t + 1] + 0.3 * model.x['S', t + 1] + 0.2 * model.x['T', t + 1] \
           + 0.4 * model.x['C', t + 2] + 0.2 * model.x['S', t + 2] + 0.1 * model.x['T', t + 2]


model.manpower_constraints = pyo.Constraint(years[1:], rule=manpower_constraint_rule)


# productive capacity constraint
def productive_capacity_constraint_rule(model, i, t):
    if t == 0:
        return model.x[i, t] <= initial_capacity[i]
    else:
        return model.x[i, t] <= initial_capacity[i] + sum(model.y[i, l] for l in range(1, t + 1))


model.productive_capacity_constraint = pyo.Constraint(industries, years[1:], rule=productive_capacity_constraint_rule)

solver = pyo.SolverFactory('cplex')
rs = solver.solve(model)

for t in years:
    for i in industries:
        print(f"Total Output of {i} in Year {t} : {model.x[i, t].value}")
