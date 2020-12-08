import functools as ft
import operator as op
import re

from typing import cast, Dict, IO, Iterator, List, Match, Tuple

TBag = List[Tuple[int, str]]


def parse(input_file: IO) -> Iterator[TBag]:
    line_regex = re.compile(r"(.+)\scontain\s(.+)\.")
    entry_regex = re.compile(r"([0-9]*)? ?(.+)?\sbags?")

    def map_entry(entry: str) -> Tuple[int, str]:
        count, bag = cast(
            Match[str], entry_regex.match(entry.strip())).groups()
        return (1 if count == '' else int(count), cast(str, bag))

    def map_line(line: str) -> TBag:
        first_bag, rest = cast(Match[str], line_regex.match(line)).groups()
        return [map_entry(first_bag)] + [map_entry(x) for x in rest.split(",")]

    yield from (map_line(line) for line in input_file)


def _roots(input_file: IO) -> Dict[str, TBag]:
    return {root[0][1]: root[1:] for root in list(parse(input_file))}


def p_1(input_file: IO,
        debug=False):  # pylint: disable=unused-argument
    roots = {key: [x[1] for x in value] for key, value in
             _roots(input_file).items()}
    roots[''] = list(roots.keys())

    def _helper(path: List[str]):
        if path[-1] == 'shiny gold':
            return set() if len(path) == 2 else {path[1]}
        return ft.reduce(op.or_, (_helper(path + [child]) for child in
                                  roots.get(path[-1], [])), set())

    return len(_helper(['']))


def p_2(input_file: IO,
        debug=False):  # pylint: disable=unused-argument
    roots = _roots(input_file)

    def _helper(nodes: TBag):
        counts = (count*_helper(roots.get(bag, [])) for count, bag in nodes)
        return 0 if not nodes else 1+ft.reduce(op.add, counts)

    return _helper(roots['shiny gold'])-1
