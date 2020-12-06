import functools as ft
import operator as op

from typing import Callable, IO, Iterator, List, Set

import aoc.common as common


def parse(input_file: IO) -> Iterator[List[Set[str]]]:
    yield from ([set(line) for line in chunk] for chunk in
                common.read_chunked(input_file))


def solve(input_file: IO,
          set_op: Callable[[Set[str], Set[str]], Set[str]]) -> int:
    return sum(len(x) for x in
               (ft.reduce(set_op, x) for x in parse(input_file)))


def p_1(input_file: IO,
        debug=False):  # pylint: disable=unused-argument
    return solve(input_file, op.or_)


def p_2(input_file: IO,
        debug=False):  # pylint: disable=unused-argument
    return solve(input_file, op.and_)
