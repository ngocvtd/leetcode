import pyomo.environ as pyo

data = {
    'retailer': ['M1', 'M2', 'M3', 'M4', 'M5', 'M6', 'M7',
                 'M8', 'M9', 'M10', 'M11', 'M12', 'M13',
                 'M14', 'M15', 'M16', 'M17', 'M18', 'M19',
                 'M20', 'M21', 'M22', 'M23'],
    'oil_market': [9, 13, 14, 17, 18, 19, 23, 21, 9, 11, 17, 18, 18,
                   17, 22, 24, 36, 43, 6, 15, 15, 25, 39],
    'delivery_points': [11, 47, 44, 25, 10, 26, 26, 54, 18, 51,
                        20, 105, 7, 16, 34, 100, 50, 21, 11, 19,
                        14, 10, 11],
    'spirit_market': [34, 411, 82, 157, 5, 183, 14, 215, 102, 21,
                      54, 0, 6, 96, 118, 112, 535, 8, 53, 28, 69, 65, 27],
    'growth_category': ['A', 'A', 'A', 'B', 'A', 'A', 'B', 'B', 'B',
                        'A', 'B', 'B', 'B', 'B', 'A', 'B', 'B', 'B',
                        'B', 'A', 'B', 'B', 'B']
}

# set of retailer
retailers = data['retailer']

# parameters
oil_market = {r: data['oil_market'][i] for i, r in enumerate(retailers)}
delivery_points = {r: data['delivery_points'][i] for i, r in enumerate(retailers)}
spirit_market = {r: data['spirit_market'][i] for i, r in enumerate(retailers)}
growth_category = {r: data['growth_category'][i] for i, r in enumerate(retailers)}

model = pyo.ConcreteModel()

model.x = pyo.Var(retailers, domain=pyo.Binary)

# constraints
model.total_delivery_points_constraint = pyo.Constraint(
    expr=sum(model.x[r] * delivery_points[r] for r in retailers) >= 0.35 * sum(delivery_points.values())
)

model.total_spirit_market_constraint = pyo.Constraint(
    expr=sum(model.x[r] * spirit_market[r] for r in retailers) >= 0.35 * sum(spirit_market.values())
)

model.region1_oil_market_constraint_min = pyo.Constraint(
    expr=0.35 * sum(oil_market[r] for r in retailers) <= sum(model.x[r] * oil_market[r] for r in retailers[:8])
)

model.region1_oil_market_constraint_max = pyo.Constraint(
    expr=sum(model.x[r] * oil_market[r] for r in retailers[:8]) <= 0.45 * sum(oil_market[r] for r in retailers)
)

model.region2_oil_market_constraint = pyo.Constraint(
    expr=sum(model.x[r] * oil_market[r] for r in retailers[8:18]) >= 0.35 * sum(oil_market[r] for r in retailers[8:18])
)

model.region3_oil_market_constraint = pyo.Constraint(
    expr=sum(model.x[r] * oil_market[r] for r in retailers[18:]) >= 0.35 * sum(oil_market[r] for r in retailers[18:])
)

model.groupA_retailer_constraint = pyo.Constraint(
    expr=sum(model.x[r] for r in retailers if growth_category[r] == 'A') >= 0.35 * sum(
        1 for r in retailers if growth_category[r] == 'A')
)

model.groupB_retailer_constraint = pyo.Constraint(
    expr=sum(model.x[r] for r in retailers if growth_category[r] == 'B') >= 0.35 * sum(
        1 for r in retailers if growth_category[r] == 'B')
)

solver = pyo.SolverFactory('cplex')
results = solver.solve(model)

if results.solver.termination_condition == pyo.TerminationCondition.optimal:
    print("Optimal Solution Found:")
    print("Division D1:")
    for r in retailers:
        if pyo.value(model.x[r]) == 1:
            print(
                f"{r} - Oil market: {oil_market[r]} , Delivery points: {delivery_points[r]}, "
                f"Spirit market: {spirit_market[r]} ")
else:
    print("No Optimal Solution Found.")
