import numpy as np
import dri
import ingredients
import argparse
import copy

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--dri', metavar='profile')
    args = parser.parse_args()

    dailyprofile = {}
    try:
        dailyprofile = getattr(dri, args.dri)
    except:
        raise Exception("Invalid DRI profile specified. Check dri.py for valid profiles.")

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
