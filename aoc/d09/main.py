import itertools as it

from typing import IO, List, Optional

import aoc.d01.main as d01


def parse(input_file: IO) -> List[int]:
    return [int(x) for x in input_file]


def _solve_part_1(numbers: List[int], preamble_len: int) -> Optional[int]:
    for idx in range(preamble_len+1, len(numbers)):
        target = numbers[idx]
        candidates = numbers[idx-preamble_len:idx]
        if d01.sum_to(sorted(candidates), target) is None:
            return target

    return None


def p_1(input_file: IO,
        debug=False):  # pylint: disable=unused-argument

    def _solve(numbers: List[int], preamble_len: int) -> Optional[int]:
        for idx in range(preamble_len+1, len(numbers)):
            target = numbers[idx]
            candidates = numbers[idx-preamble_len:idx]
            if d01.sum_to(sorted(candidates), target) is None:
                return target

        return None

    return _solve(parse(input_file), 25)


def p_2(input_file: IO,
        debug=False):  # pylint: disable=unused-argument
    def _solve(numbers: List[int], preamble_len: int) -> Optional[int]:
        target = _solve_part_1(numbers, preamble_len)

        if not target:
            return None

        cum_sum = list(it.accumulate(numbers))

        for i, _ in enumerate(cum_sum):
            for j in range(i+2, len(cum_sum)):
                if cum_sum[j]-cum_sum[i] == target:
                    contiguous_range = numbers[i+1:j+1]
                    return min(contiguous_range)+max(contiguous_range)

        return None

    return _solve(parse(input_file), 25)
