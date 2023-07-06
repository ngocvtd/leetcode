import pyomo.environ as pyo

model = pyo.ConcreteModel()
model.x_1 = pyo.Var(within=pyo.NonNegativeReals)
model.x_2 = pyo.Var(within=pyo.NonNegativeReals)
model.obj = pyo.Objective(expr=model.x_1 + 2*model.x_2)
model.con1 = pyo.Constraint(expr=3*model.x_1 + 4*model.x_2 >= 1)
model.con2 = pyo.Constraint(expr=2*model.x_1 + 5*model.x_2 >= 2)

solver = pyo.SolverFactory('cplex')
result = solver.solve(model)

if result.solver.termination_condition == pyo.TerminationCondition.optimal:
    print("Giá trị tối ưu của biến x_1:", pyo.value(model.x_1))
    print("Giá trị tối ưu của biến x_2:", pyo.value(model.x_2))
    print("Giá trị tối ưu của hàm mục tiêu:", pyo.value(model.obj))
else:
    print("Không tìm thấy nghiệm tối ưu.")
