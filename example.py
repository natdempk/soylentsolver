from linear_solver import pywraplp
def main(unused_argv):
    # using GLPK
  solver = pywraplp.Solver('CoinsGridGLPK',
          pywraplp.Solver.GLPK_LINEAR_PROGRAMMING)

  # Using CLP
  # solver = pywraplp.Solver('CoinsGridCLP',
  #                          pywraplp.Solver.CLP_LINEAR_PROGRAMMING)

  n =  31  # the grid size
  c =  14  # number of coins per row/column

  x = {}
  for i in range(n):
      for j in range(n):
          x[(i,j)] = solver.IntVar(0, 1, 'x[%i,%i]' % (i, j))

  # sum rows/columns == c
  for i in range(n):
      solver.Add(solver.Sum(
          [x[(i, j)] for j in range(n)]) == c)      # sum rows
      solver.Add(solver.Sum(
          [x[(j, i)] for j in range(n)]) == c) # sum cols

      # quadratic horizonal distance var
  objective_var = solver.Sum(
          [x[(i, j)] * (i - j) * (i - j)
              for i in range(n) for j in range(n)])

          objective = solver.Minimize(objective_var)

  solver.Solve()

  for i in range(n):
      for j in range(n):
          # int representation
      print int(x[(i, j)].solution_value()),
    print
  print

if __name__ == '__main__':
    main("coin grids")
