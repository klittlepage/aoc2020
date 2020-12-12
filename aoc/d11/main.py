import itertools as it

from enum import Enum
from typing import Callable, IO, Iterator, List


class State(Enum):
    FLOOR = '.'
    EMPTY = 'L'
    OCCUPIED = '#'


TGrid = List[List[State]]


def parse(input_file: IO) -> TGrid:
    def as_enum(x: str) -> State:
        if x == State.FLOOR.value:
            return State.FLOOR
        if x == State.EMPTY.value:
            return State.EMPTY
        if x == State.OCCUPIED.value:
            return State.OCCUPIED

        assert False
        return None

    return [[as_enum(x) for x in row.strip()] for row in input_file]


TAdjacencies = Callable[[TGrid, int, int], Iterator[State]]


def transition_rule(grid: TGrid,
                    row: int,
                    col: int,
                    adjacencies: TAdjacencies,
                    thresh: int) -> State:
    cur_state = grid[row][col]
    adjacency_list = list(adjacencies(grid, row, col))
    if cur_state == State.EMPTY and \
            sum(1 for x in adjacency_list if x == State.OCCUPIED) == 0:
        return State.OCCUPIED

    if cur_state == State.OCCUPIED and \
            sum(1 for x in adjacency_list if x == State.OCCUPIED) >= thresh:
        return State.EMPTY

    return cur_state


def _step(grid: TGrid, adjacencies: TAdjacencies, thresh: int) -> TGrid:
    return [[transition_rule(grid, row, col, adjacencies, thresh) for col, _
             in enumerate(grid[row])] for
            row, _ in enumerate(grid)]


def _fixed_point(grid: TGrid, adjacencies: TAdjacencies, thresh: int) -> TGrid:
    starting_grid = grid
    transformed_grid = _step(starting_grid, adjacencies, thresh)

    while starting_grid != transformed_grid:
        starting_grid = transformed_grid
        transformed_grid = _step(starting_grid, adjacencies, thresh)

    return transformed_grid


def _count_occupied(grid: TGrid) -> int:
    return sum(sum(1 if x == State.OCCUPIED else 0 for x in row) for row in
               grid)


def p_1(input_file: IO,
        debug=False):  # pylint: disable=unused-argument

    def adjacencies(grid: TGrid, row: int, col: int) -> Iterator[State]:
        for d_x, d_y in it.product(range(-1, 2), range(-1, 2)):
            if d_x == 0 and d_y == 0:
                continue

            x = col+d_x
            y = row+d_y
            if 0 <= x < len(grid[row]) and 0 <= y < len(grid):
                yield grid[y][x]

    return _count_occupied(_fixed_point(parse(input_file), adjacencies, 4))


def p_2(input_file: IO,
        debug=False):  # pylint: disable=unused-argument

    def adjacencies(grid: TGrid, row: int, col: int) -> Iterator[State]:
        n_rows = len(grid)
        n_cols = len(grid[row])
        for d_x, d_y in it.product(range(-1, 2), range(-1, 2)):
            if d_x == 0 and d_y == 0:
                continue

            x = col+d_x
            y = row+d_y
            adjacency = State.FLOOR

            while 0 <= x < n_cols and 0 <= y < n_rows:
                neighbor = grid[y][x]
                if neighbor in [State.OCCUPIED, State.EMPTY]:
                    adjacency = neighbor
                    break

                x += d_x
                y += d_y

            yield adjacency

    return _count_occupied(_fixed_point(parse(input_file), adjacencies, 5))
