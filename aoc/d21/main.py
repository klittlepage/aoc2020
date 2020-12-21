import functools as ft
import itertools as it
import operator as op
import re

from typing import Dict, IO, List, Tuple

from ortools.linear_solver import pywraplp  # type: ignore

TRecipe = Tuple[List[str], List[str]]


def parse(input_file: IO) -> List[TRecipe]:
    match_expr = re.compile(r"^(.+) \(contains (.+)\)$")

    def parse_line(line: str) -> Tuple[List[str], List[str]]:
        match = match_expr.match(line)
        assert match
        ingredients = match.group(1).split(' ')
        allergens = [x.strip() for x in match.group(2).split(',')]
        return ingredients, allergens

    return [parse_line(x.strip()) for x in input_file]


def find_allergens(recipes: List[TRecipe]) -> Dict[str, str]:
    ingredients = set(x for x in it.chain.from_iterable(x[0] for x in recipes))
    allergens = set(x for x in it.chain.from_iterable(x[1] for x in recipes))

    solver = pywraplp.Solver.CreateSolver('SCIP')
    variables = dict()

    for ingredient, allergen in it.product(ingredients, allergens):
        variables[(ingredient, allergen)] = \
            solver.IntVar(0, 1, f"{ingredient}_{allergen}")

    for recipe_ingredients, recipe_allergens in recipes:
        for recipe_allergen in recipe_allergens:
            # All allergens in a recipe must be in exactly one ingredient in
            # the recipe
            constraint = [variables[(recipe_ingredient, recipe_allergen)] for
                          recipe_ingredient in recipe_ingredients]
            solver.Add(ft.reduce(op.add, constraint) == 1)

    for ingredient in ingredients:
        # Each ingredient contains at most one allergen
        constraint = [variables[(ingredient, allergen)] for
                      allergen in allergens]
        solver.Add(ft.reduce(op.add, constraint) <= 1)

    for allergen in allergens:
        # Each allergen is present in exactly one ingredient
        constraint = [variables[(ingredient, allergen)] for
                      ingredient in ingredients]
        solver.Add(ft.reduce(op.add, constraint) == 1)

    # Arbitrary choice of objective, given that we're only interested in
    # SAT
    solver.Maximize(ft.reduce(op.add, variables.values()))
    status = solver.Solve()

    ingredients_with_allergens = dict()
    if status == pywraplp.Solver.OPTIMAL:
        for ((ingredient, allergen)), outcome_var in variables.items():
            if outcome_var.solution_value() > 0:
                ingredients_with_allergens[ingredient] = allergen
    else:
        raise Exception('no solution found')

    return ingredients_with_allergens


def p_1(input_file: IO,
        debug=False):  # pylint: disable=unused-argument
    recipes = parse(input_file)
    ingredients = set(x for x in it.chain.from_iterable(x[0] for x in recipes))
    allergens = find_allergens(recipes)
    safe_ingredients = {x for x in ingredients if x not in allergens}

    return sum(1 if x in safe_ingredients else 0 for x in
               it.chain.from_iterable((x[0] for x in recipes)))


def p_2(input_file: IO,
        debug=False):  # pylint: disable=unused-argument
    allergens = sorted(find_allergens(parse(input_file)).items(),
                       key=op.itemgetter(1))
    return ','.join(x[0] for x in allergens)
