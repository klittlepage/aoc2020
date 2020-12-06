import functools as ft
import operator as op

from typing import Callable, IO, Iterator, List, Set


def parse(input_file: IO) -> Iterator[List[Set[str]]]:
    questions: List[Set[str]] = list()

    for row in input_file:
        if row == '\n':
            yield questions
            questions = list()
        else:
            questions.append((set(row.strip())))

    if questions:
        yield questions


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
