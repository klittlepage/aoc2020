import functools as ft

from typing import Callable, IO, Iterable, List


def parse(input_file: IO) -> Iterable[List[bool]]:
    for line in input_file:
        yield [x in ['B', 'R'] for x in line.strip()]


def bisect(binary_coordinates: List[bool], upper_bound: int) -> int:
    def reducer(acc, x):
        lower, upper = acc
        mid = (lower+upper)//2
        return (mid+1, upper) if x else (lower, mid)

    lower, upper = ft.reduce(reducer, binary_coordinates, (0, upper_bound))
    assert lower == upper
    return lower


def extrema(coords: Iterable[List[bool]],
            func: Callable[[Iterable[int]], int]) -> int:
    return func(to_index(row) for row in coords)


def to_index(row: List[bool]) -> int:
    return 8*bisect(row[0:7], 127) + bisect(row[7:], 7)


def p_1(input_file: IO,
        debug=False):  # pylint: disable=unused-argument
    return extrema(parse(input_file), max)


def p_2(input_file: IO,
        debug=False):  # pylint: disable=unused-argument
    parsed = list(parse(input_file))
    unoccupied_seats = \
        set(range(extrema(parsed, min), extrema(parsed, max)+1)) - \
        set(to_index(row) for row in parsed)

    assert len(unoccupied_seats) == 1
    return next(iter(unoccupied_seats))
