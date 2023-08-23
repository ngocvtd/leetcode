import pyomo.environ as pyo

# Tổng số tháng
months = range(6)  # 0 to 5

# Danh sách dầu
oils = ['VEG1', 'VEG2', 'OIL1', 'OIL2', 'OIL3']

# Chi phí mua dầu trong mỗi tháng
costs = {
    ('VEG1', 0): 110, ('VEG1', 1): 130, ('VEG1', 2): 110,
    ('VEG1', 3): 120, ('VEG1', 4): 100, ('VEG1', 5): 90,
    ('VEG2', 0): 120, ('VEG2', 1): 130, ('VEG2', 2): 140,
    ('VEG2', 3): 110, ('VEG2', 4): 120, ('VEG2', 5): 100,
    ('OIL1', 0): 130, ('OIL1', 1): 110, ('OIL1', 2): 130,
    ('OIL1', 3): 120, ('OIL1', 4): 150, ('OIL1', 5): 140,
    ('OIL2', 0): 110, ('OIL2', 1): 90, ('OIL2', 2): 100,
    ('OIL2', 3): 120, ('OIL2', 4): 110, ('OIL2', 5): 80,
    ('OIL3', 0): 115, ('OIL3', 1): 115, ('OIL3', 2): 95,
    ('OIL3', 3): 125, ('OIL3', 4): 105, ('OIL3', 5): 135,
}

# Lượng sản phẩm cuối cùng bán ra và lợi nhuận
selling_price = 150
profit_per_ton = selling_price - 5  # Sản xuất giá £150, lưu trữ chi phí £5

# Độ cứng của từng loại dầu
hardness_values = {'VEG1': 8.8, 'VEG2': 6.1, 'OIL1': 2.0, 'OIL2': 4.2, 'OIL3': 5.0}

# Tạo mô hình Pyomo
model = pyo.ConcreteModel()

# Biến mua, sử dụng và lưu trữ dầu
model.buy_vars = pyo.Var(oils, months, within=pyo.NonNegativeReals)
model.use_vars = pyo.Var(oils, months, within=pyo.NonNegativeReals)
model.store_vars = pyo.Var(oils, months, within=pyo.NonNegativeReals)

# Biến sản xuất sản phẩm cuối cùng
model.prod_vars = pyo.Var(months, within=pyo.NonNegativeReals)
model.hardness_vars = pyo.Var(months, within=pyo.Reals)

# Ràng buộc về mua, sử dụng và lưu trữ dầu
model.buy_constraints = pyo.ConstraintList()
for oil in oils:
    for month in months:
        if month == 0:
            # Ràng buộc khởi tạo lượng dầu lưu trữ
            model.buy_constraints.add(model.store_vars[oil, month] == 500)
        else:
            # Ràng buộc lượng dầu lưu trữ qua các tháng
            model.buy_constraints.add(
                model.store_vars[oil, month] == model.store_vars[oil, month - 1] + model.buy_vars[oil, month] -
                model.use_vars[oil, month])

# Ràng buộc về khả năng sản xuất
model.capacity_constraints = pyo.ConstraintList()
for month in months:
    model.capacity_constraints.add(
        sum(model.use_vars[oil, month] for oil in oils if oil.startswith("VEG")) <= 200
    )
    model.capacity_constraints.add(
        sum(model.use_vars[oil, month] for oil in oils if oil.startswith("OIL")) <= 250
    )

# Ràng buộc về độ cứng sản phẩm cuối cùng
# Ràng buộc về độ cứng sản phẩm cuối cùng
model.hardness_constraints = pyo.ConstraintList()
for month in months:
    hardness_expr = sum(model.use_vars[oil, month] * hardness_values[oil] for oil in oils)
    # Sử dụng biến độ cứng tính toán trong ràng buộc
    model.hardness_constraints.add(model.hardness_vars[month] >= 3)
    model.hardness_constraints.add(model.hardness_vars[month] <= 6)
    # Ràng buộc giữa độ cứng tính toán và biểu thức thực tế
    model.hardness_constraints.add(model.hardness_vars[month] == hardness_expr)

# Giải quyết mô hình tối ưu
solver = pyo.SolverFactory('cplex')
results = solver.solve(model)

## Kiểm tra xem giải quyết có hợp lệ không
if results.solver.termination_condition == pyo.TerminationCondition.optimal:
    print("Optimal solution found!")
    print("Oil quantities for each month:")
    for month in months:
        print(f"Month {month}:")
        for oil in oils:
            buy_var = model.buy_vars[oil, month]
            use_var = model.use_vars[oil, month]
            store_var = model.store_vars[oil, month]

            buy_quantity = buy_var.value if buy_var.value is not None else 0.0
            use_quantity = use_var.value if use_var.value is not None else 0.0
            store_quantity = store_var.value if store_var.value is not None else 0.0

            print(f"  {oil}:")
            print(f"    Buy: {buy_quantity:.2f} tons")
            print(f"    Use: {use_quantity:.2f} tons")
            print(f"    Store: {store_quantity:.2f} tons")
else:
    print("No optimal solution found.")
