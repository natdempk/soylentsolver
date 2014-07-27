import dri
import ingredients
import argparse
import copy
import sys
import string
import pprint
from constraint import *

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--dri', metavar='profile')
    parser.add_argument('--list-dri', action='store_true')
    args = parser.parse_args()

    if args.list_dri:
        noprint = ['__builtins__', '__doc__', '__file__', '__name__', '__package__']
        print "Available DRIs:"
        for d in dir(dri):
            if not d in noprint:
                print d
        sys.exit(0)

    dailyprofile = {}
    try:
        dailyprofile = getattr(dri, args.dri)
    except: raise Exception("Invalid DRI profile specified. Check dri.py for valid profiles.")

    problem = Problem()
    #problem = Problem(RecursiveBacktrackingSolver())
    #problem = Problem(MinConflictsSolver())

    #for ingredient in ingredients.ingredients:
        #problem.addVariable(ingredient['name'], range(1000)) # range(1000) will be so slow :(

    ingredient_names = [ing['name'] for ing in ingredients.ingredients]
    for name in ingredient_names:
        problem.addVariable(name, range(6000))


    for nutrient, amount in dailyprofile.iteritems():
        nutr_min = None
        nutr_max = None
        if type(amount) is tuple:
            nutr_min, nutr_max = amount
        else:
            nutr_min = amount
        nutr_letters = []
        nutr_conds = []
        nutr_vars = []
        for ingredient, letter in zip(ingredients.ingredients, string.ascii_lowercase[:len(ingredients.ingredients)]):
            try:
                number = float(ingredient[nutrient])/float(ingredient['serving_size'])
                nutr_conds.append("{}*{!s}".format(letter, number))
                #nutr_conds.append("{}*{!s}/{!s}".format(letter, float(ingredient[nutrient]), float(ingredient['serving_size'])))
                nutr_letters.append(letter)
                nutr_vars.append(ingredient['name'])
            except:
                pass

        letters_str = ', '.join(nutr_letters)
        conds_str = ' + '.join(nutr_conds)
        #vars_tup = nutr_vars
        #nutr_f_str = 'lambda {}: ({}) >= {}'.format(letters_str, conds_str, amount)
        nutr_f_str = 'lambda {}: ({}) >= {}'.format(letters_str, conds_str, nutr_min)
        nutr_f = eval(nutr_f_str)

        print nutr_vars
        print nutr_f_str
        print nutrient
        problem.addConstraint(nutr_f, nutr_vars)

        #if nutr_max:
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
    pprint.pprint(problem._constraints)
    print(type(problem.getSolver()))

    sol = problem.getSolutionIter()
    #sol = problem.getSolution()
    for x in xrange(25):
        print(sol.next())
    #print sol
    sys.exit()
