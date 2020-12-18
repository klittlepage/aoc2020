import itertools as it

from typing import cast, Dict, IO, Iterator, List, Tuple

TCoord = Tuple[int, ...]
TGrid = Dict[Tuple[int, ...], bool]
TRange = Tuple[int, int]


def parse(input_file: IO, dimensions: int) -> TGrid:
    grid = dict()
    for y_idx, row in enumerate(input_file):
        for x_idx, col in enumerate(row.strip()):
            coord = tuple([x_idx, y_idx] + (dimensions-2)*[0])
            grid[coord] = col == '#'
    return grid


def neighbors(grid: TGrid,
              coordinate: TCoord) -> Iterator[bool]:
    for delta in it.product(*[range(-1, 2) for _ in coordinate]):
        if all(x == 0 for x in delta):
            continue

        n = cast(TCoord, tuple([c+dv for c, dv in zip(coordinate, delta)]))
        yield grid.get(n, False)


def coordinate_extrema(grid: TGrid, dimensions: int) -> List[TRange]:
    coordinates = [coord for coord, value in grid.items() if value]
    min_values = [min((coord[dim] for coord in coordinates), default=0) for
                  dim in range(dimensions)]
    max_values = [max((coord[dim] for coord in coordinates), default=0) for
                  dim in range(dimensions)]
    return list(zip(min_values, max_values))


def coordinate_ranges(extrema: List[TRange], delta: int) -> List[TRange]:
    return [(a-delta, b+delta+1) for a, b in extrema]


def print_grid(grid: TGrid, dimensions: int):
    ranges = coordinate_ranges(coordinate_extrema(grid, dimensions), 0)

    for higher_order_dims in it.product(*[range(*x) for x in
                                          reversed(ranges[2:])]):
        print(higher_order_dims)
        for y in range(*ranges[1]):
            for x in range(*ranges[0]):
                coord = cast(TCoord, tuple([x, y] + list(higher_order_dims)))
                print('#' if grid.get(coord, False) else '.', end='')
            print()
        print()


def update_grid(grid: TGrid, dimensions: int) -> TGrid:
    updated_grid = dict()
    ranges = coordinate_ranges(coordinate_extrema(grid, dimensions), 1)

    for coord in (cast(TCoord, x) for x in
                  it.product(*(range(*x) for x in ranges))):
        neighbor_count = sum(neighbors(grid, coord))
        if grid.get(coord, False):
            updated_grid[coord] = neighbor_count in [2, 3]
        else:
            updated_grid[coord] = neighbor_count == 3

    return updated_grid


def run(input_file: IO, dimensions: int) -> int:
    grid = parse(input_file, dimensions)

    for _ in range(6):
        grid = update_grid(grid, dimensions)

    return sum(grid.values())


def p_1(input_file: IO,
        debug=False):  # pylint: disable=unused-argument
    return run(input_file, 3)


def p_2(input_file: IO,
        debug=False):  # pylint: disable=unused-argument
    return run(input_file, 4)
