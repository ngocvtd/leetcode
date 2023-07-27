import pyomo.environ as pyo

contribution = [10, 6, 8, 4, 11, 9, 3]

production_time_grinder = [0.5, 0.7, 0, 0, 0.3, 0.2, 0.5]
production_time_vertical_drill = [0.1, 0.2, 0, 0.3, 0, 0.6, 0]
production_time_horizontal_drill = [0.2, 0, 0.8, 0, 0, 0, 0.6]
production_time_borer = [0.05, 0.03, 0, 0.07, 0.1, 0, 0.08]
production_time_planer = [0, 0, 0.01, 0, 0.05, 0, 0.05]

market_demand = [
    [500, 1000, 300, 300, 800, 200, 100],
    [600, 500, 200, 0, 400, 300, 150],
    [300, 600, 0, 0, 500, 400, 100],
    [200, 300, 400, 500, 200, 0, 100],
    [0, 100, 500, 100, 1000, 300, 0],
    [500, 500, 100, 300, 1100, 500, 60]
]

demand_prod1 = [500, 600, 300, 200, 0, 500]
demand_prod2 = [1000, 500, 600, 300, 100, 500]
demand_prod3 = [300, 200, 0, 400, 500, 100]
demand_prod4 = [300, 0, 0, 500, 100, 300]
demand_prod5 = [800, 400, 500, 200, 1000, 1100]
demand_prod6 = [200, 300, 400, 0, 300, 500]
demand_prod7 = [100, 150, 100, 100, 0, 60]

num_products = len(contribution)
num_months = len(market_demand)

# the number of grinders available each month
num_grinders = [3, 4, 4, 4, 3, 4]
num_vertical_drills = [2, 2, 2, 1, 1, 2]
num_horizontal_drills = [3, 1, 3, 3, 3, 2]
num_borer = [1, 1, 0, 1, 1, 1]
num_planer = [1, 1, 1, 1, 1, 0]

model = pyo.ConcreteModel()

# manu - facture
model.M = pyo.Var(range(num_products), range(num_months), domain=pyo.NonNegativeReals)
# sold
model.S = pyo.Var(range(num_products), range(num_months), domain=pyo.NonNegativeReals)
# held
model.H = pyo.Var(range(num_products), range(num_months), domain=pyo.NonNegativeReals)
model.GR = pyo.Var()
# obj function
model.profit = pyo.Objective(
    expr=sum(
        model.S[i, j] * contribution[i] - 0.5 * model.H[i, j] for i in range(num_products) for j in range(num_months)),
    sense=pyo.maximize
)


# constraints
# grinder constraint
def grinder_production_constraint(model, j):
    return sum(model.M[i, j] * production_time_grinder[i] for i in range(num_products)) <= num_grinders[j] * 24 * 16


def vertical_drill_production_constraint(model, j):
    return sum(model.M[i, j] * production_time_vertical_drill[i] for i in range(num_products)) <= num_vertical_drills[
        j] * 24 * 6


def horizontal_drill_production_constraint(model, j):
    return sum(model.M[i, j] * production_time_horizontal_drill[i] for i in range(num_products)) <= \
           num_horizontal_drills[
               j] * 24 * 8


def borer_production_constraint(model, j):
    return sum(model.M[i, j] * production_time_borer[i] for i in range(num_products)) <= num_borer[j] * 24 * 8


def planer_production_constraint(model, j):
    return sum(model.M[i, j] * production_time_planer[i] for i in range(num_products)) <= num_planer[j] * 24 * 8


model.grinder_time = pyo.Constraint(range(num_months), rule=grinder_production_constraint)
model.vertical_time = pyo.Constraint(range(num_months), rule=vertical_drill_production_constraint)
model.horizontal_time = pyo.Constraint(range(num_months), rule=horizontal_drill_production_constraint)
model.borer_time = pyo.Constraint(range(num_months), rule=borer_production_constraint)
model.planer_time = pyo.Constraint(range(num_months), rule=planer_production_constraint)


# balance constraint
def balance_rule(model, i, j):
    if j > 0:
        return model.M[i, j] + model.H[i, j - 1] == model.S[i, j] + model.H[i, j]
    else:
        return model.M[i, j] == model.S[i, j] + model.H[i, j]


model.balance_constraints = pyo.Constraint(range(num_products), range(num_months), rule=balance_rule)


def storage_capacity_rule(model, i, j):
    return model.H[i, j] <= 100


model.storage_constraints = pyo.Constraint(range(num_products), range(num_months), rule=storage_capacity_rule)


def final_month_stock_rule(model, i):
    return model.H[i, num_months - 1] == 50


model.final_month_stock_constraints = pyo.Constraint(range(num_months),
                                                     rule=final_month_stock_rule)


def market_demand_constraint(model, i, j):
    return model.S[i, j] <= market_demand[j][i]


model.market_demand_constraints = pyo.Constraint(range(num_products), range(num_months), rule=market_demand_constraint)


def final_month_stock_rule_prod7(model):
    return model.H[6, num_months - 1] == 50


model.final_month_stock_constraint_prod7 = pyo.Constraint(rule=final_month_stock_rule_prod7)



def print_results_per_month(model):
    for j in range(num_months):
        print(f"\nTháng {j + 1}:")
        print("Sản phẩm được sản xuất (M):")
        for i in range(num_products):
            print(f"Sản phẩm {i + 1}: {model.M[i, j]()}")

        print("\nSản phẩm được bán (S):")
        for i in range(num_products):
            print(f"Sản phẩm {i + 1}: {model.S[i, j]()}")

        print("\nSản phẩm tồn kho (H):")
        for i in range(num_products):
            print(f"Sản phẩm {i + 1}: {model.H[i, j]()}")


# Tối ưu hóa mô hình
solver = pyo.SolverFactory('cplex')
results = solver.solve(model)

# In kết quả tối ưu
if results.solver.termination_condition == pyo.TerminationCondition.optimal:
    print("Tối ưu hóa thành công!")
    print("Tổng lợi nhuận tối đa:", model.profit())
    print_results_per_month(model)
else:
    print("Không tìm thấy lời giải tối ưu.")
