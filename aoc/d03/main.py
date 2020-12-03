import functools as ft
import itertools as it
import operator as op

from typing import List, IO

TGrid = List[List[bool]]


def parse(input_file: IO) -> TGrid:
    return [[x == '#' for x in row.strip()] for row in input_file]


def traverse(grid: TGrid, rise: int, run: int) -> int:
    def is_tree():
        for row, col in zip(grid[rise::rise], it.count(run, run)):
            yield row[col % len(grid[0])]

    return sum(is_tree())


def p_1(input_file: IO,
        debug=False):  # pylint: disable=unused-argument
    return traverse(parse(input_file), 1, 3)


def p_2(input_file: IO,
        debug=False):  # pylint: disable=unused-argument
    slopes = [
        [1, 1],
        [1, 3],
        [1, 5],
        [1, 7],
        [2, 1],
    ]
    grid = parse(input_file)
    return ft.reduce(op.mul, (traverse(grid, *slope) for slope in slopes))
