from typing import Dict, List, Iterator, IO, Tuple

from aoc.common import search


def parse(input_file: IO) -> List[int]:
    return [int(x) for x in input_file]


def p_1(input_file: IO,
        debug=False):  # pylint: disable=unused-argument
    def p_1_search() -> Iterator[List[int]]:
        def reject(_state: List[int], _partial: List[int]) -> bool:
            return False

        def accept(state: List[int], _partial: List[int]) -> bool:
            return not state

        def next_candidate(state: List[int], partial: List[int]) -> \
                Iterator[Tuple[List[int], List[int]]]:
            for idx, value in enumerate(state):
                if not (value > partial[-1] and value-partial[-1] <= 3):
                    break

                new_state = state[:idx] + state[idx+1:]
                new_candidate = partial+[value]

                yield (new_state, new_candidate)

        adapters = sorted(parse(input_file))
        starting_state = adapters + [adapters[-1]+3]
        first_candidate = [0]

        yield from search.backtracking(reject, accept, next_candidate,
                                       starting_state, first_candidate)

    results = list(p_1_search())
    assert len(results) == 1
    chain = results[0]
    diff = [t-s for s, t in zip(chain, chain[1:])]
    return sum(1 for x in diff if x == 1) * sum(1 for x in diff if x == 3)


def p_2(input_file: IO,
        debug=False):  # pylint: disable=unused-argument
    cache: Dict[int, int] = dict()

    def _arrangements(state: List[int], target: int) -> int:
        if target < 1:
            return 1

        if target in cache:
            return cache[target]

        n = len(state)
        total = 0
        for idx, value in enumerate(reversed(state)):
            if not (value < target and target-value <= 3):
                break

            total += _arrangements(state[:n-idx-1] + state[n-idx+1:], value)

        cache[target] = total
        return total

    adapters = sorted(parse(input_file))
    return _arrangements([0] + adapters, adapters[-1]+3)
