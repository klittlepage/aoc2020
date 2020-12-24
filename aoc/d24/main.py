import functools as ft
import itertools as it

from collections import deque
from typing import cast, Dict, IO, Iterator, List, Tuple

TCoord = Tuple[int, int, int]


def cube_directions() -> Dict[str, TCoord]:
    directions = {
        'e': (1, -1, 0),
        'se': (0, -1, 1),
        'sw': (-1, 0, 1),
        'w': (-1, 1, 0),
        'nw': (0, 1, -1),
        'ne': (1, 0, -1)
    }

    return directions


def cube_add(coord: TCoord, offset: TCoord) -> TCoord:
    return cast(TCoord, tuple((c+delta) for c, delta in zip(coord, offset)))


def parse(input_file: IO) -> List[List[str]]:
    def parse_line(line: str) -> Iterator[str]:
        tokens = deque(list(line))

        while tokens:
            t_1 = tokens.popleft()
            assert t_1 in ['e', 'w', 's', 'n']
            if t_1 in ['e', 'w']:
                yield t_1
            elif t_1 in ['s', 'n']:
                t_2 = tokens.popleft()
                assert t_2 in ['e', 'w']
                yield f"{t_1}{t_2}"

    return [list(parse_line(x.strip())) for x in input_file]


def initial_configuration(input_file: IO) -> Dict[TCoord, bool]:
    directions = cube_directions()

    def reducer(acc: Dict[TCoord, bool],
                instructions: List[str]) -> Dict[TCoord, bool]:
        destination = ft.reduce(lambda acc, x: cube_add(acc, directions[x]),
                                instructions, (0, 0, 0))
        acc[destination] = not acc.get(destination, False)
        return acc

    return ft.reduce(reducer, parse(input_file), dict())


def p_1(input_file: IO,
        debug=False):  # pylint: disable=unused-argument
    return sum(initial_configuration(input_file).values())


def p_2(input_file: IO,
        debug=False):  # pylint: disable=unused-argument
    offsets = cube_directions()

    def map_tile(tiles: Dict[TCoord, bool], coord: TCoord, state: bool) -> bool:
        total = sum(tiles.get(cube_add(coord, offset), False)
                    for offset in offsets.values())
        return not (total == 0 or total > 2) if state else total == 2

    def reducer(tiles: Dict[TCoord, bool], _x: int) -> Dict[TCoord, bool]:
        neighbors = set(x for x in (cube_add(coord, offset) for coord, offset in
                                    it.product(tiles.keys(), offsets.values())))
        tiles.update((x, False) for x in neighbors if x not in tiles)
        return {coord: map_tile(tiles, coord, state) for coord, state in
                tiles.items()}

    return sum(ft.reduce(reducer, range(100),
                         initial_configuration(input_file)).values())
