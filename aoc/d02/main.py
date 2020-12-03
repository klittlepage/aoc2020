import dataclasses
import re

from collections import Counter
from typing import IO, List


@dataclasses.dataclass
class Policy:
    min_count: int
    max_count: int
    letter: str
    password: str


def parse(input_file: IO) -> List[Policy]:
    entry_regex = re.compile(r"([0-9]+)-([0-9]+)\s([a-zA-Z]):\s([a-zA-z]+)")

    def _map_entry(entry: str) -> Policy:
        match = entry_regex.match(entry)
        if match is None:
            raise ValueError(entry)

        (min_count, max_count, letter, password) = match.groups()
        return Policy(int(min_count), int(max_count), letter, password)

    return [_map_entry(x) for x in input_file.readlines()]


def p_1(input_file: IO,
        debug=False):  # pylint: disable=unused-argument

    def is_valid(policy: Policy) -> bool:
        counts = Counter(policy.password)
        if policy.letter not in counts:
            return False

        letter_count = counts[policy.letter]
        return policy.min_count <= letter_count <= policy.max_count

    return sum(is_valid(x) for x in parse(input_file))


def p_2(input_file: IO,
        debug=False):  # pylint: disable=unused-argument

    def is_valid(policy: Policy) -> bool:
        return (policy.password[policy.min_count-1] == policy.letter) ^ \
               (policy.password[policy.max_count-1] == policy.letter)

    return sum(is_valid(x) for x in parse(input_file))
