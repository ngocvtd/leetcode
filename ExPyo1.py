import pyomo.environ as pyo

model = pyo.ConcreteModel()
model.A = pyo.Set(initialize=[1,2,3])
model.B = pyo.Set(initialize=['Q', 'R'])
model.x = pyo.Var()
model.y = pyo.Var(model.A, model.B)
model.o = pyo.Objective(expr=model.x)

def d_rule(model, a):
    return a * model.x <= 0
model.d = pyo.Constraint(model.A, rule=d_rule)

solver = pyo.SolverFactory('cplex')
result = solver.solve(model)

if result.solver.termination_condition == pyo.TerminationCondition.optimal:
    print("Giá trị tối ưu của biến x:", pyo.value(model.x))
    print("Giá trị tối ưu của biến y:", pyo.value(model.y))
    print("Giá trị tối ưu của hàm mục tiêu:", pyo.value(model.o))
else:
    print("Không tìm thấy nghiệm tối ưu.")