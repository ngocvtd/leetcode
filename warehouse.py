import pyomo.environ as pyo

def create_warehouse_model(N, M, d, P):
  model = pyo.ConcreteModel(name="(WL)")

  model.x = pyo.Var(N, M, bounds=(0,1))
  model.y = pyo.Var(N, within=pyo.Binary)

  def obj_rule(mdl):
    return sum(d[n,m]*mdl.x[n,m] for n in N for m in M)
  model.obj = pyo.Objective(rule=obj_rule)

  def demand_rule(mdl, m):
    return sum(mdl.x[n,m] for n in N) == 1
  model.demand = pyo.Constraint(M, rule=demand_rule)

  def warehouse_active_rule(mdl, n, m):
    return mdl.x[n,m] <= mdl.y[n]
  model.warehouse_active = pyo.Constraint(N, M, \
    rule=warehouse_active_rule)

  def num_warehouses_rule(mdl):
    return sum(mdl.y[n] for n in N) <= P
  model.num_warehouses = \
    pyo.Constraint(rule=num_warehouses_rule)

  return model

N = ['Harlingen', 'Memphis', 'Ashland']
M = ['NYC', 'LA', 'Chicago', 'Houston']

d = {
    ('Harlingen', 'NYC'): 1956,
    ('Harlingen', 'LA'): 1606,
    ('Harlingen', 'Chicago'): 1410,
    ('Harlingen', 'Houston'): 330,
    ('Memphis', 'NYC'): 1096,
    ('Memphis', 'LA'): 1972,
    ('Memphis', 'Chicago'): 531,
    ('Memphis', 'Houston'): 567,
    ('Ashland', 'NYC'): 485,
    ('Ashland', 'LA'): 2322,
    ('Ashland', 'Chicago'): 324,
    ('Ashland', 'Houston'): 1236
}
P = 2
model = create_warehouse_model(N, M, d, P)
solver = pyo.SolverFactory('cplex')
res = solver.solve(model)
pyo.assert_optimal_termination(res)
model.y.pprint()
