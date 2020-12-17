import dataclasses
import functools as ft
import itertools as it
import operator as op
import re

from typing import cast, IO, Iterator, List, Optional, Set, Tuple

import aoc.common.search as search

TConstraint = Tuple[Tuple[int, int], Tuple[int, int]]
TState = Tuple[Set[int], Set[int]]
TAssignment = Tuple[str, int]
TAssignments = List[TAssignment]


@dataclasses.dataclass
class _Problem:
    fields: List[Tuple[str, TConstraint]]
    ticket: List[int]
    other_tickets: List[List[int]]

    def is_invalid(self, value) -> bool:
        for _, ((lb_1, ub_1), (lb_2, ub_2)) in self.fields:
            if lb_1 <= value <= ub_1 or lb_2 <= value <= ub_2:
                return False

        return True


def parse(input_file: IO) -> _Problem:
    field_regex = \
        re.compile(r"^([\w\s]+): ([0-9]+)\-([0-9]+) or ([0-9]+)\-([0-9]+)$")

    fields = list()
    while True:
        line = input_file.readline()
        if line == '\n':
            break
        match = field_regex.match(line)
        if not match:
            raise Exception('expected a field')

        name, lb_1, ub_1, lb_2, ub_2 = match.groups()
        fields.append((name, ((int(lb_1), int(ub_1)), (int(lb_2), int(ub_2)))))

    assert input_file.readline() == 'your ticket:\n'

    ticket = [int(x) for x in input_file.readline().strip().split(',')]

    input_file.readline()
    assert input_file.readline() == 'nearby tickets:\n'

    other_tickets = [[int(x) for x in line.strip().split(',')] for
                     line in input_file]

    return _Problem(fields, ticket, other_tickets)


def p_1(input_file: IO,
        debug=False):  # pylint: disable=unused-argument
    problem = parse(input_file)
    return sum(x if problem.is_invalid(x) else 0 for x in
               it.chain(*problem.other_tickets))


def p_2(input_file: IO,
        debug=False):  # pylint: disable=unused-argument
    def check_constraint(constraint: TConstraint,
                         value: int) -> bool:
        ((lb_1, ub_1), (lb_2, ub_2)) = constraint
        return lb_1 <= value <= ub_1 or lb_2 <= value <= ub_2

    def is_legal_assignment(problem: _Problem,
                            constraint: TConstraint,
                            field: int) -> bool:
        if not check_constraint(constraint, problem.ticket[field]):
            return False

        for neighbor in problem.other_tickets:
            if not check_constraint(constraint, neighbor[field]):
                return False

        return True

    def legal_assignments(problem: _Problem,
                          constraint: TConstraint) -> List[int]:
        return [field for field in range(len(problem.ticket)) if
                is_legal_assignment(problem, constraint, field)]

    problem = parse(input_file)
    valid_neighbors = [ticket for ticket in problem.other_tickets if not
                       sum(problem.is_invalid(field) for field in ticket)]
    problem = _Problem(problem.fields, problem.ticket, valid_neighbors)
    legal_for_field = [(idx, name, legal_assignments(problem, constraint)) for
                       idx, (name, constraint) in enumerate(problem.fields)]
    legal_for_field.sort(key=lambda x: len(x[2]))

    def unassigned() -> Set[int]:
        return {idx for idx, _ in enumerate(problem.ticket)}

    def find_most_constrained(unassigned_fields: Set[int]) -> \
            Optional[Tuple[int, str, List[int]]]:
        for (idx, name, myopic_legal) in legal_for_field:
            if idx in unassigned_fields:
                return idx, name, myopic_legal

        return None

    def accept(state: TState, _assignment: TAssignments) -> bool:
        unassigned_fields, unassigned_cols = state
        return not (unassigned_fields or unassigned_cols)

    def reject(_state: TState, _assignment: TAssignments) -> bool:
        return False

    def next_candidate(state: TState, assignment: TAssignments) -> \
            Iterator[Tuple[TState, TAssignments]]:
        unassigned_fields, unassigned_cols = state
        most_constrained = find_most_constrained(unassigned_fields)
        if most_constrained:
            field_idx, name, myopic_legal = most_constrained
            for next_assignment in myopic_legal:
                if next_assignment not in unassigned_cols:
                    continue

                yield ({x for x in unassigned_fields if x != field_idx},
                       {x for x in unassigned_cols if x != next_assignment}), \
                    assignment[:] + [(name, problem.ticket[next_assignment])]

    res = list(search.backtracking(reject,
                                   accept,
                                   next_candidate,
                                   (unassigned(), unassigned()),
                                   cast(TAssignments, list())))

    assert len(res) == 1
    assignment = res[0]

    return ft.reduce(op.mul, (value for name, value in assignment if
                              name.startswith('departure')), 1)
