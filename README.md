soylentsolver
=============

A hacker-friendly tool to create optimal soylent recipes from an ingredient set using a constraint solver.

## Usage

First you should probably create a Python 2.7 `virtualenv` for this project and clone/fork it.

Next install the required Python packages by running

    $ pip install -r requirements.txt
    
from the project directory.

Additionally install `ortools` by running

    $ easy_install ortools

Then you can either set up your own DRI (Dietary Reference Intake) or use one of the one's provided in `dri.py`.
If you wish to set up your own, just copy/modify an already existing one from `dri.py`. 
A nutrient with just a single number is assumed to have no daily intake limit, while a tuple represents the `(min, max)` daily intake values.

Once you have a DRI, you can add some ingredients to `ingredients.py` to geneate your recipe from.
All ingredients in `ingredients.py` will be used to generate the recipe.
Ingredients can be added as `dicts` to the `ingredients` `list`.
Any nutrient that is not specified for an ingredient is assumed to be `0`.
It is also important to give your ingredients unique names or the solver will likely break.
The serving size is represented in grams, and all other nutrients are listed in the units specified on http://diy.soylent.me.
If you need to know the key to use for a nutrient, all possible nutrients are listed in `dri.py`.

Once you have your list of ingredients, you can run the solver to generate a recipe.
You must provide a DRI as follows:

    $ python soylentsolver.py --dri usg_m_2700
    
You can see a full list of available flags with:

    $ python soylentsolver.py --help

## Planned Features

- Make the solver actually work. `or-tools` may be a failure...
- Rank recipes by closeness to DRI, maybe multiple iterations to find most optimal recipes.
- Flag to minimize number of ingredients
- Potentially integration with http://diy.soylent.me so that recipes and DRI's can be automatically pushed/pulled.
