import pyomo.environ as pyo
import time

model = pyo.ConcreteModel()

# Tạo biến
model.X1 = pyo.Var(domain=pyo.NonNegativeReals)
model.X2 = pyo.Var(domain=pyo.NonNegativeReals)
model.X3 = pyo.Var(domain=pyo.NonNegativeReals)
model.X4 = pyo.Var(domain=pyo.NonNegativeReals)
model.X5 = pyo.Var(domain=pyo.NonNegativeReals)
model.Y1 = pyo.Var(domain=pyo.NonNegativeReals)
model.Y2 = pyo.Var(domain=pyo.NonNegativeReals)
model.Y3 = pyo.Var(domain=pyo.NonNegativeReals)
model.Y4 = pyo.Var(domain=pyo.NonNegativeReals)
model.Y5 = pyo.Var(domain=pyo.NonNegativeReals)

# Hàm mục tiêu
model.profit = pyo.Objective(
    expr=(150 * model.X1 + 150 * model.X2 + 150 * model.X3 + 150 * model.X4 + 150 * model.X5)
    - (110 * model.Y1 + 120 * model.Y2 + 130 * model.Y3 + 110 * model.Y4 + 115 * model.Y5)
    - (5 * (model.Y1 + model.Y2 + model.Y3 + model.Y4 + model.Y5)),
    sense=pyo.maximize
)

# Ràng buộc
model.constraints = pyo.ConstraintList()

# Khả năng tinh chế
model.constraints.add(model.X1 + model.Y1 <= 200)
model.constraints.add(model.X2 + model.Y2 <= 200)
model.constraints.add(model.X3 + model.Y3 <= 250)
model.constraints.add(model.X4 + model.Y4 <= 250)
model.constraints.add(model.X5 + model.Y5 <= 250)

# Lưu trữ
model.constraints.add(model.Y1 <= 1000)
model.constraints.add(model.Y2 <= 1000)
model.constraints.add(model.Y3 <= 1000)
model.constraints.add(model.Y4 <= 1000)
model.constraints.add(model.Y5 <= 1000)

# Độ cứng sản phẩm
model.constraints.add(
    8.8 * model.X1 + 6.1 * model.X2 + 2.0 * model.X3 + 4.2 * model.X4 + 5.0 * model.X5
    == 6 * (model.X1 + model.X2 + model.X3 + model.X4 + model.X5)
)

# Tồn kho
model.constraints.add(model.Y1 + model.Y2 + model.Y3 + model.Y4 + model.Y5 == 500)

solver = pyo.SolverFactory('cplex')

start_time = time.time()
solver.solve(model)
end_time = time.time()

print("Optimal profit:", pyo.value(model.profit))
print("Tons of VEG 1 purchased:", pyo.value(model.X1))
print("Tons of VEG 2 purchased:", pyo.value(model.X2))
print("Tons of OIL 1 purchased:", pyo.value(model.X3))
print("Tons of OIL 2 purchased:", pyo.value(model.X4))
print("Tons of OIL 3 purchased:", pyo.value(model.X5))
print("Tons of VEG 1 from storage used:", pyo.value(model.Y1))
print("Tons of VEG 2 from storage used:", pyo.value(model.Y2))
print("Tons of OIL 1 from storage used:", pyo.value(model.Y3))
print("Tons of OIL 2 from storage used:", pyo.value(model.Y4))
print("Tons of OIL 3 from storage used:", pyo.value(model.Y5))
print("Time run:", end_time - start_time, "s")


