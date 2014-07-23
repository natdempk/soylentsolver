import numpy as np
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
    except:
        raise Exception("Invalid DRI profile specified. Check dri.py for valid profiles.")

    problem = Problem()
    #for ingredient in ingredients.ingredients:
        #problem.addVariable(ingredient['name'], range(1000)) # range(1000) will be so slow :(

    ingredient_names = [ing['name'] for ing in ingredients.ingredients]
    for name in ingredient_names:
        problem.addVariable(name, range(1000))


    # TODO: the issue here is that dict is not hashable so it cant be used in nutr_vars...
    # this means that the dict should probably be turned into somethign hashable before use
    # like a tuple namedtuple or list or something
    for nutrient, amount in dailyprofile.iteritems():
        nutr_letters = []
        nutr_conds = []
        nutr_vars = []
        for ingredient, letter in zip(ingredients.ingredients, string.ascii_lowercase[:len(ingredients.ingredients)]):
            try:
                nutr_conds.append("{}*{!s}/{!s}".format(letter, float(ingredient[nutrient]), float(ingredient['serving_size'])))
                nutr_letters.append(letter)
                nutr_vars.append(ingredient)
            except:
                pass

        letters_str = ', '.join(nutr_letters)
        conds_str = ' + '.join(nutr_conds)
        #vars_tup = nutr_vars
        nutr_f_str = 'lambda {}: {} >= {}'.format(letters_str, conds_str, amount)
        nutr_f = eval(nutr_f_str)

        problem.addConstraint(nutr_f, nutr_vars)

        #for ingredient in ingredients.ingredients:

        # add constraint of eval'd nutr_f

    print problem
    print dir(problem)
    print "============== VARIABLES"
    pprint.pprint(problem._variables)
    print "============== CONSTRAINTS"
    pprint.pprint(problem._constraints)

    sol = problem.getSolution()
    print sol





    ####


    goal = []
    for k in sorted(dailyprofile.keys()):
        # construct ordered solution matrix of nutrients
        goal.append(float(dailyprofile[k]))
    goal_arr = np.array(goal)

    ingrs = []
    for x in dailyprofile.keys():
        ingrs.append(list())
    for i, ing in enumerate(ingredients.ingredients):
        #ingrs.append(list())
        #nutrs = ingrs[i]
        ingredient = copy.copy(ing) 
        del ingredient['name']
        ss = float(ingredient['serving_size'])
        del ingredient['serving_size']
        #nutrs = []
        # create matrix rep of ingredients
        for i, k in enumerate(sorted(dailyprofile.keys())):
            try:
                amnt = ingredient[k]
                ingrs[i].append(float(amnt)/ss)
            except:
                ingrs[i].append(float(0.0))
        #ingrs.append(nutrs)

    print goal
    print len(goal)
    print ingrs
    print len(ingrs)

    ingrs_arr = np.array(ingrs)
    sol = np.linalg.lstsq(ingrs_arr, goal_arr)
    #sol = np.linalg.lstsq(goal_arr, ingrs_arr)
    print sol
    #for i, k in sorted(dailyprofile.keys()):
        #print k + ' : ' + sol[i]
    for i, ing in enumerate(ingredients.ingredients):
        print ing['name']  + ' ' + str(sol[i])
        pass
