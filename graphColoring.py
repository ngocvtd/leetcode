# data for the graph of interest
vertices = set(['Ar', 'Bo', 'Br', 'Ch', 'Co', 'Ec',
                'FG', 'Gu', 'Pa', 'Pe', 'Su', 'Ur', 'Ve'])

edges = set([('FG','Su'), ('FG','Br'), ('Su','Gu'),
             ('Su','Br'), ('Gu','Ve'), ('Gu','Br'),
             ('Ve','Co'), ('Ve','Br'), ('Co','Ec'),
             ('Co','Pe'), ('Co','Br'), ('Ec','Pe'),
             ('Pe','Ch'), ('Pe','Bo'), ('Pe','Br'),
             ('Ch','Ar'), ('Ch','Bo'), ('Ar','Ur'),
             ('Ar','Br'), ('Ar','Pa'), ('Ar', 'Bo'),
             ('Ur','Br'), ('Bo','Pa'), ('Bo', 'Br'),
             ('Pa','Br')])

ncolors = 4
colors = range(1, ncolors+1)

# import statement
import pyomo.environ as pyo

# Create a Pyomo model object
model = pyo.ConcreteModel()

# Define model variables
model.x = pyo.Var(vertices, colors, within=pyo.Binary)
model.y = pyo.Var()

# Each node is clored with one color
model.node_coloring = pyo.ConstraintList()
for v in vertices:
    model.node_coloring.add(sum(model.x[v,c] for c in colors)==1)

# Nodes that share an edge cannot be colored the same
model.edge_coloring = pyo.ConstraintList()
for v, w in edges:
    for c in colors:
        model.edge_coloring.add(model.x[v,c] + model.x[w,c] <=1)

# Provide a lower bound on the minimum number of colors that are needed
model.min_coloring = pyo.ConstraintList()
for v in vertices:
    for c in colors:
        model.min_coloring.add(model.y >= c * model.x[v,c])

# Minimize the number of colors that are needed
model.obj = pyo.Objective(expr=model.y)
solver = pyo.SolverFactory('cplex')
result = solver.solve(model)

print(pyo.value(model.obj))