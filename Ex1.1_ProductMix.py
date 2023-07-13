import pyomo.environ as pyo

model = pyo.ConcreteModel()

model.x1 = pyo.Var(domain=pyo.NonNegativeIntegers)
model.x2 = pyo.Var(domain=pyo.NonNegativeIntegers)
model.x3 = pyo.Var(domain=pyo.NonNegativeIntegers)
model.x4 = pyo.Var(domain=pyo.NonNegativeIntegers)
model.x5 = pyo.Var(domain=pyo.NonNegativeIntegers)

# hàm mục tiêu
model.obj = pyo.Objective(expr=550*model.x1 +600*model.x2 + 350*model.x3 + 400*model.x4 + 200+model.x5)

# ràng buộc thời gian
model.con1 = pyo.Constraint(expr= 12*model.x1 + 20*model.x2 + 25*model.x4 + 15*model.x5 <= 288)
model.con2 = pyo.Constraint(expr= 20*model.x1 + 8*model.x2 + 16*model.x3 <= 192)

solve = pyo.SolverFactory('cplex')
solve.solve(model)

print("Optimal profit:", pyo.value(model.obj))
print("PROD1:", pyo.value(model.x1))
print("PROD2:", pyo.value(model.x2))
print("PROD3:", pyo.value(model.x3))
print("PROD4:", pyo.value(model.x4))
print("PROD5:", pyo.value(model.x5))
