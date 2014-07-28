import dri
import ingredients
import argparse
import copy
import sys
import string
import pprint
import operator
#from constraint import *
from ortools.constraint_solver import pywrapcp

if __name__ == '__main__':
    # define and parse arguments
    parser = argparse.ArgumentParser()
    parser.add_argument('--dri', metavar='profile')
    parser.add_argument('--list-dri', action='store_true')
    args = parser.parse_args()

    if args.list_dri: # display available DRIs
        noprint = ['__builtins__', '__doc__', '__file__', '__name__', '__package__']
        print "Available DRIs:"
        for d in dir(dri):
            if not d in noprint:
                print d
        print "Additional DRIs can be specified by editing dri.py"
        sys.exit(0)

    dailyprofile = {} # check DRI validity
    try:
        dailyprofile = getattr(dri, args.dri)
    except: raise Exception("Invalid DRI profile specified. Check dri.py for valid profiles.")

    # create solver
    solver = pywrapcp.Solver("Soylent")
    #problem = Problem()
    #problem = Problem(RecursiveBacktrackingSolver())
    #problem = Problem(MinConflictsSolver())

    #for ingredient in ingredients.ingredients:
        #problem.addVariable(ingredient['name'], range(1000)) # range(1000) will be so slow :(

    #[solver_vars[name] = problem.IntVar(range(1000), name) for name in ingredient_names] 
    
    # create solver variables
    ingredient_names = [ing['name'] for ing in ingredients.ingredients]
    solver_vars = {}

    for name in ingredient_names:
        solver_vars[name] = solver.IntVar(range(1000), name)
        #problem.addVariable(name, range(6000))
        #problem.IntVar(range(1000), str(name))

    # create constraints for solver
    for nutrient, amount in dailyprofile.iteritems():
        nutr_min = None
        nutr_max = None
        if type(amount) is tuple:
            nutr_min, nutr_max = amount
        else:
            nutr_min = amount

        nutr_letters = []
        nutr_conds = []
        ###
        nutr_vars = []
        nutr_nums = []
        ###
        for ingredient, letter in zip(ingredients.ingredients, string.ascii_lowercase[:len(ingredients.ingredients)]):
            try:
                number = float(ingredient[nutrient])/float(ingredient['serving_size'])
                nutr_vars.append(solver_vars[ingredient['name']])
                nutr_nums.append(number)
                #nutr_conds.append("{}*{!s}".format(letter, number))
                #nutr_conds.append("{}*{!s}/{!s}".format(letter, float(ingredient[nutrient]), float(ingredient['serving_size'])))
                #nutr_letters.append(letter)
                #nutr_vars.append(ingredient['name'])
            except: # skip ingredients that don't have the nutrient in them
                pass

        #mul_exps = [operator.mul(*t) for t in zip(nutr_vars, nutr_nums)]
        mul_exps = [solver.ScalProd(*t) for t in zip(nutr_vars, nutr_nums)]
        #for t in zip(nutr_vars, nutr_nums):
            
        solver.Add(solver.Sum(mul_exps) >= nutr_min)

        #letters_str = ', '.join(nutr_letters)
        #conds_str = ' + '.join(nutr_conds)
        #vars_tup = nutr_vars
        #nutr_f_str = 'lambda {}: ({}) >= {}'.format(letters_str, conds_str, amount)
        #nutr_f_str = 'lambda {}: ({}) >= {}'.format(letters_str, conds_str, nutr_min)
        #nutr_f = eval(nutr_f_str)

        #print nutr_vars
        #print nutr_f_str
        #print nutrient
        #problem.addConstraint(nutr_f, nutr_vars)

        if nutr_max:
            solver.Add(solver.Sum(mul_exps) < nutr_max)
            #nutr_f_max_str = 'lambda {}: ({}) < {}'.format(letters_str, conds_str, nutr_max)
            #nutr_f_max = eval(nutr_f_max_str)
            #print nutr_vars
            #print nutr_f_max_str
            #print nutrient
            #problem.addConstraint(nutr_f_max, nutr_vars)


        #for ingredient in ingredients.ingredients:

        # add constraint of eval'd nutr_f

    #print problem
    #print dir(problem)
    #print "============== VARIABLES"
    #pprint.pprint(problem._variables)
    print "============== CONSTRAINTS"
    #pprint.pprint(problem._constraints)
    #print(type(problem.getSolver()))
    all_solutions = solver.AllSolutionCollector()
    #
    variables = [v for k, v in solver_vars.iteritems()]
    all_solutions.Add(variables)

    db = solver.Phase(variables, solver.INT_VAR_SIMPLE, solver.INT_VALUE_SIMPLE)

    time_limit = solver.TimeLimit(420) # 7 mins
    solver.Solve(db, all_solutions, time_limit)
    num_solutions = all_solutions.SolutionCount()
    print "num_solutions:", num_solutions
    print "failures:", solver.Failures()
    print "branches:", solver.Branches()
    print "WallTime:", solver.WallTime()

    #sol = problem.getSolutionIter()
    #sol = problem.getSolution()
    #for x in xrange(25):
        #print(sol.next())
    #print sol
