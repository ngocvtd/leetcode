import pyomo.environ as pyo

def IC_model(A, h, d, c, b, u):

    model = pyo.ConcreteModel(name="(H)")

    def x_bounds(m, i):
        return (0, u[i])
    model.x = pyo.Var(A, bounds=x_bounds)

    def z_rule(model):
        return sum(h[i] * (model.x[i] - (model.x[i]/d[i])**2) for i in A)
    model.z = pyo.Objective(rule=z_rule, sense=pyo.maximize)

    model.budgetconstr = pyo.Constraint(
        expr= sum(c[i] * model.x[i] for i in A) <= b
    )

    return model

A = ['I_C_Scoops', 'Peanuts']
h = {'I_C_Scoops': 1, 'Peanuts': 0.1}
d = {'I_C_Scoops': 5, 'Peanuts': 27}
c = {'I_C_Scoops': 3.14, 'Peanuts': 0.2718}
b = 12
u = {'I_C_Scoops': 100, 'Peanuts': 40.6}

model = IC_model(A, h, d, c, b, u)
solver = pyo.SolverFactory('cplex')
result = solver.solve(model)

if result.solver.termination_condition == pyo.TerminationCondition.optimal:
    print("Giá trị tối ưu của biến x:")
    for i in A:
        print(f"x[{i}] =", pyo.value(model.x[i]))
    print("Giá trị tối ưu của hàm mục tiêu:", pyo.value(model.z))
else:
    print("Không tìm thấy nghiệm tối ưu.")


