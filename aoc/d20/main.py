"""
There are eight planar symmetries of a square:

Rotation: R_0, R_90, R_180, R_270
Reflection about the horizontal axis
Reflection about the vertical axis
Reflection about the main diagonal
Reflection about the secondary diagonal

The composition of two symmetries (functions) is closed and associative, and
has an identity, and an inverse. As such, the symmetries of a square are a
group (D_4, or the dihedral group of order 8) and we only need to consider
the fundamental planar symmetries - not arbitrary combinations of them
"""

import copy
import functools as ft
import itertools as it
import math
import operator as op
import re

from collections import defaultdict, deque
from typing import (cast, Deque, Dict, IO, Iterator, List, Optional, Set, Tuple,
                    TypeVar)

import aoc.common.helpers as helpers

TTile = TypeVar('TTile', bound='Tile')
TAlignment = Dict[Tuple[int, int], TTile]

SEA_MONSTER = """
                  # 
#    ##    ##    ###
 #  #  #  #  #  #   
"""[1:-1]


class Tile:
    index: int
    tile: List[List[str]]
    _n: int

    def __init__(self, index: int, tile: List[List[str]]):
        assert len(tile) == len(tile[0])
        self.index = index
        self.tile = copy.deepcopy(tile)
        self._n = len(tile)

    def _empty_grid(self) -> List[List[str]]:
        return [['' for _ in range(self.n)] for _ in range(self.n)]

    def rotate_0(self: TTile) -> TTile:
        return copy.deepcopy(self)

    def rotate_90(self: TTile) -> TTile:
        new_tile = copy.deepcopy(self)
        for row_idx in range(self.n):
            for col_idx in range(self.n):
                new_tile.tile[row_idx][col_idx] = \
                    self.tile[self.n-col_idx-1][row_idx]

        return new_tile

    def rotate_180(self: TTile) -> TTile:
        new_tile = copy.deepcopy(self)
        for row_idx in range(self.n):
            for col_idx in range(self.n):
                new_tile.tile[row_idx][col_idx] = \
                    self.tile[self.n-row_idx-1][self.n-col_idx-1]

        return new_tile

    def rotate_270(self: TTile) -> TTile:
        new_tile = copy.deepcopy(self)
        for row_idx in range(self.n):
            for col_idx in range(self.n):
                new_tile.tile[row_idx][col_idx] = \
                    self.tile[col_idx][self.n-row_idx-1]

        return new_tile

    def reflect_horizontal(self: TTile) -> TTile:
        new_tile = copy.deepcopy(self)
        for row_idx in range(self.n):
            for col_idx in range(self.n):
                new_tile.tile[row_idx][col_idx] = \
                    self.tile[self.n-row_idx-1][col_idx]

        return new_tile

    def reflect_vertical(self: TTile) -> TTile:
        new_tile = copy.deepcopy(self)
        for row_idx in range(self.n):
            for col_idx in range(self.n):
                new_tile.tile[row_idx][col_idx] = \
                    self.tile[row_idx][self.n-col_idx-1]

        return new_tile

    def reflect_primary_diagonal(self: TTile) -> TTile:
        new_tile = copy.deepcopy(self)
        for row_idx in range(self.n):
            for col_idx in range(self.n):
                new_tile.tile[row_idx][col_idx] = \
                    self.tile[self.n-col_idx-1][self.n-row_idx-1]

        return new_tile

    def reflect_secondary_diagonal(self: TTile) -> TTile:
        new_tile = copy.deepcopy(self)
        for row_idx in range(self.n):
            for col_idx in range(self.n):
                new_tile.tile[row_idx][col_idx] = self.tile[col_idx][row_idx]

        return new_tile

    def all_symmetries(self: TTile) -> Iterator[TTile]:
        yield self.rotate_0()
        yield self.rotate_90()
        yield self.rotate_180()
        yield self.rotate_270()
        yield self.reflect_horizontal()
        yield self.reflect_vertical()
        yield self.reflect_primary_diagonal()
        yield self.reflect_secondary_diagonal()

    def strip_borders(self: TTile) -> TTile:
        new_grid = [row[1:-1] for row in self.tile[1:-1]]
        return cast(TTile, Tile(self.index, new_grid))

    @property
    def n(self) -> int:
        return self._n

    def row(self, index: int) -> List[str]:
        return self.tile[index][:]

    def col(self, index: int) -> List[str]:
        return [self.tile[row][index] for row in range(self.n)]

    def left(self) -> List[str]:
        return self.col(0)

    def right(self) -> List[str]:
        return self.col(self.n-1)

    def top(self) -> List[str]:
        return self.row(0)

    def bottom(self) -> List[str]:
        return self.row(self.n-1)

    @property
    def edges(self) -> List[str]:
        return [
            ''.join(self.row(0)),
            ''.join(self.col(self.n-1)),
            ''.join(self.row(self.n-1)),
            ''.join(self.col(0))
        ]

    def __repr__(self) -> str:
        rep_list = [
            f"index: {self.index}",
            ''
        ]

        rep_list += [''.join(row) for row in self.tile]
        rep_list += ['']
        return '\n'.join(rep_list)

    def __str__(self) -> str:
        return repr(self)


def parse(input_file: IO) -> List[Tile]:
    tile_regex = re.compile(r"Tile ([0-9]+):")

    def map_block(chunk):
        match = tile_regex.match(chunk[0])
        index = int(match.group(1))
        return Tile(index, [list(x) for x in chunk[1:]])

    return [map_block(x) for x in helpers.read_chunked(input_file)]


def canonical_edge(edge) -> str:
    return sorted([edge, edge[::-1]])[0]


def edge_map(tiles: List[Tile]) -> Dict[str, Set[int]]:
    edges = defaultdict(set)

    for tile in tiles:
        for edge in tile.edges:
            edges[canonical_edge(edge)].add(tile.index)

    return dict(edges)


def edge_counts(tiles: List[Tile], edges: Dict[str, Set[int]]) -> \
        List[Tuple[int, int]]:
    return [(tile.index, sum(len(edges[canonical_edge(x)]) for x
                             in tile.edges)) for tile in tiles]


def corners(tiles: List[Tile]) -> List[int]:
    edges = edge_map(tiles)
    counts = edge_counts(tiles, edges)
    corner_tiles = [x[0] for x in counts if x[1] == 6]
    assert len(corner_tiles) == 4
    return corner_tiles


def solve_alignment(tiles: List[Tile]) -> Optional[TAlignment]:
    tile_map = {x.index: x for x in tiles}

    max_grid_idx = int(math.sqrt(len(tiles)))
    search_stack: Deque[Tuple[TAlignment, Set[int], int]] = deque()

    for corner in tile_map[corners(tiles)[0]].all_symmetries():
        initial = ({(0, 0): corner}, set(tile_map.keys()) - {corner.index}, 1)
        search_stack.append(initial)

    while search_stack:
        solution, unplaced_tiles, idx = search_stack.pop()

        if not unplaced_tiles:
            return solution

        x, y = divmod(idx, max_grid_idx)

        for tile in it.chain.from_iterable(tile_map[idx].all_symmetries() for
                                           idx in unplaced_tiles):
            if x-1 >= 0:
                neighbor = solution[(x-1, y)]
                if tile.left() != neighbor.right():
                    continue
            if y-1 >= 0:
                neighbor = solution[(x, y-1)]
                if tile.bottom() != neighbor.top():
                    continue

            updated_solution = copy.copy(solution)
            updated_solution[(x, y)] = tile
            updated_unplaced_tiles = set(unplaced_tiles) - {tile.index}

            search_stack.append((updated_solution, updated_unplaced_tiles,
                                 idx+1))

    return None


def alignment_tile(alignment: TAlignment) -> Tile:
    n = int(math.sqrt(len(alignment)))
    grid = [['' for _ in range(n)] for _ in range(n)]
    for ((x, y), value) in alignment.items():
        grid[y][x] = f" {value.index} "

    return Tile(0, grid)


def merge_tiles(alignment: TAlignment) -> Tile:
    square_size = next(iter(alignment.values())).n-2
    grid_size = int(math.sqrt(len(alignment)))
    grid: List[List[str]] = [list() for _ in range(grid_size*square_size)]

    for ((_x, y), value) in sorted(alignment.items(),
                                   key=lambda x: (x[0][1], x[0][0])):
        square = value.rotate_90().strip_borders()
        sub_grid = grid[y*square_size:(y+1)*square_size]
        for merged_row, row in zip(sub_grid, square.tile):
            merged_row.extend(row)

    return Tile(0, grid)


def all_grids(input_file: IO) -> Iterator[Tile]:
    tiles = parse(input_file)

    alignment = solve_alignment(tiles)
    if not alignment:
        raise Exception('no alignment found')

    verify_alignment(alignment)
    aligned_tiles = {v.index: v for v in alignment.values()}

    for oriented_alignment in alignment_tile(alignment).all_symmetries():
        transform = [[int(x.strip()) for x in row] for row in
                     oriented_alignment.tile]

        transformed_alignment = dict()
        for y, row in enumerate(transform):
            for x, index in enumerate(row):
                transformed_alignment[(x, y)] = aligned_tiles[index]

        yield merge_tiles(transformed_alignment)


def count_monsters(tile: TTile) -> int:
    template = [list(x) for x in SEA_MONSTER.split('\n')]
    n_rows = len(template)
    n_cols = len(template[0])

    def template_match(sub_grid):
        for template_row, grid_row in zip(template, sub_grid):
            for template_entry, grid_entry in zip(template_row, grid_row):
                if template_entry == '#' and grid_entry != '#':
                    return False

        return True

    def count_helper():
        for y in range(tile.n-n_rows):
            for x in range(tile.n-n_cols):
                sub_grid = [row[x:x+n_cols] for row in tile.tile[y:y+n_rows]]
                yield template_match(sub_grid)

    return sum(count_helper())


def verify_alignment(alignment: TAlignment):
    max_x = max(alignment.keys(), key=lambda x: x[0])[0]
    max_y = max(alignment.keys(), key=lambda x: x[1])[1]
    assert max_x == max_y
    assert (max_x+1)**2 == len(alignment)

    for ((x, y), value) in alignment.items():
        for d_x, d_y in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
            if 0 <= x+d_x <= max_x and 0 <= y+d_y <= max_y:
                neighbor = alignment[(x+d_x, y+d_y)]
                if d_x == -1 and d_y == 0:
                    assert neighbor.right() == value.left()
                if d_x == 1 and d_y == 0:
                    assert neighbor.left() == value.right()
                if d_x == 0 and d_y == -1:
                    assert neighbor.top() == value.bottom()
                if d_x == 0 and d_y == 1:
                    assert neighbor.bottom() == value.top()


def p_1(input_file: IO,
        debug=False):  # pylint: disable=unused-argument
    tiles = parse(input_file)
    return ft.reduce(op.mul, corners(tiles))


def p_2(input_file: IO,
        debug=False):  # pylint: disable=unused-argument
    tiles_per_monster = sum(sum(x == '#' for x in row) for row in
                            SEA_MONSTER.split('\n'))

    def _helper():
        for grid in all_grids(input_file):
            for oriented_grid in grid.all_symmetries():
                n_monsters = count_monsters(oriented_grid)
                if n_monsters != 0:
                    grid_count = sum(sum(x == '#' for x in row) for row in
                                     oriented_grid.tile)
                    yield grid_count - n_monsters*tiles_per_monster

    return min(_helper(), default=None)
