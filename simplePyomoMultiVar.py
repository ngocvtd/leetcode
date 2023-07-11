import pyomo.environ as pyo
import time

model = pyo.ConcreteModel()

# Định nghĩa biến quyết định
model.x = pyo.Var(range(1, 11), within=pyo.NonNegativeReals)

# Hàm mục tiêu
model.obj = pyo.Objective(expr=sum(2 * model.x[i] for i in range(1, 6)) + sum(3 * model.x[i] for i in range(6, 11)), sense=pyo.maximize)

# Ràng buộc
model.con1 = pyo.Constraint(expr=sum(model.x[i] for i in range(1, 6)) <= 200)
model.con2 = pyo.Constraint(expr=sum(model.x[i] for i in range(6, 11)) <= 250)
model.con3 = pyo.Constraint(expr=sum(model.x[i] for i in range(1, 6)) >= 150)
model.con4 = pyo.Constraint(expr=model.x[1] + model.x[2] + model.x[3] >= 50)
model.con5 = pyo.Constraint(expr=model.x[4] + model.x[5] >= 30)

# Khởi tạo solver
solver = pyo.SolverFactory('cplex')

# Bắt đầu đếm thời gian
start_time = time.time()

# Giải bài toán tối ưu
result = solver.solve(model)

# Kết thúc đếm thời gian
end_time = time.time()

# In kết quả
if result.solver.termination_condition == pyo.TerminationCondition.optimal:
    print("Giá trị tối ưu của hàm mục tiêu:", pyo.value(model.obj))
    for i in range(1, 11):
        print("Giá trị tối ưu của biến x{}: {}".format(i, pyo.value(model.x[i])))
    print("Thời gian chạy:", end_time - start_time, "giây")
else:
    print("Không tìm thấy nghiệm tối ưu.")


