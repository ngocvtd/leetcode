import pyomo.environ as pyo

# create a standard python dict for mapping subsquares to the list (row, col) entries
subsq_to_row_col = dict()

subsq_to_row_col[1] = [(i,j) for i in range(1,4) for j in range(1,4)]
subsq_to_row_col[2] = [(i,j) for i in range(1,4) for j in range(4,7)]
subsq_to_row_col[3] = [(i,j) for i in range(1,4) for j in range(7,10)]

subsq_to_row_col[4] = [(i,j) for i in range(4,7) for j in range(1,4)]
subsq_to_row_col[5] = [(i,j) for i in range(4,7) for j in range(4,7)]
subsq_to_row_col[6] = [(i,j) for i in range(4,7) for j in range(7,10)]

subsq_to_row_col[7] = [(i,j) for i in range(7,10) for j in range(1,4)]
subsq_to_row_col[8] = [(i,j) for i in range(7,10) for j in range(4,7)]
subsq_to_row_col[9] = [(i,j) for i in range(7,10) for j in range(7,10)]

def create_sodoku_model(board):

    model = pyo.ConcreteModel()

    # store the starting board for the model
    model.board = board

    # create sets for rows columns and squares
    model.ROWS = pyo.RangeSet(1,9)
    model.COLS = pyo.RangeSet(1,9)
    model.VALUES = pyo.RangeSet(1,9)
    model.SUBSQUARES = pyo.RangeSet(1,9)

    # create the binary variables to define the values
    model.y = pyo.Var(model.ROWS, model.COLS, model.VALUES, within=pyo.Binary)

    # fix variables based on the current board
    for (r,c,v) in board:
        model.y[r,c,v].fix(1)

    # create the obj - this is a feasibility problem
    # so we just make it a constant
    model.obj = pyo.Objective(expr=1.0)

    # exactly one number in each row
    def _RowCon(model, r, v):
        return sum(model.y[c,r,v] for c in model.COLS) == 1
    model.RowCon = pyo.Constraint(model.COLS, model.ROWS, rule=_RowCon)

    # exactly one number in each colum
    def _ColCon(model, c, v):
        return sum(model.y[c,r,v] for r in model.ROWS) == 1
    model.ColCon = pyo.Constraint(model.COLS, model.VALUES, rule=_ColCon)

    # exactly one number in each subsquare
    def _SqCon(model, s, v):
        return sum(model.y[c,r,v] for (r,c) in subsq_to_row_col[s]) == 1
    model.SqCon = pyo.Constraint(model.SUBSQUARES, model.VALUES, rule=_SqCon)

    # exactly one number in each cell
    def _ValueCon(model, r, c):
        return sum(model.y[c,r,v] for v in model.VALUES) == 1
    model.ValueCon = pyo.Constraint(model.ROWS, model.COLS, rule=_ValueCon)

    return model

# use this function to add a new integer cut to the model
def add_integer_cut(model):
    # add the ConstraintList to store IntegerCuts if
    # it does not already exist
    if not hasattr(model, "IntegerCust"):
        model.IntegerCuts = pyo.ConstraintList()

    # add the integer cut corresponding to the current
    # solution in the model
    cut_expr = 0.0
    for r in model.ROWS:
        for c in model.COLS:
            for v in model.VALUES:
                if not model.y[c,r,v].fixed:
                    if pyo.value(model.y[c,r,v]) >= 0.5:
                        cut_expr += (1.0 - model.y[r,c,v])
                    else:
                        cut_expr -= model.y[c,r,v]

    model.IntegerCuts.add(cut_expr >= 1)

# prints the current solution stored in the model
def print_solution(model):
    for r in model.ROWS:
        print(''.join(str(v) for c in model.COLS for v in model.VALUES
                      if pyo.value(model.y[c,r,v]) >= 0.5))
