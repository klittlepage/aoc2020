from collections import deque

from typing import Deque, IO, List


def parse(input_file: IO) -> List[int]:
    return list(int(x) for x in list(input_file.read().strip()))


def play_game(initial_cups: List[int], max_cup: int, rounds: int) -> List[int]:
    input_size = len(initial_cups)
    cups = [0 for _ in range(max_cup + 1)]
    current_idx = initial_cups[0]

    for idx in range(1, len(initial_cups)):
        cups[current_idx] = initial_cups[idx]
        current_idx = cups[current_idx]

    for idx in range(input_size+1, max_cup+1):
        cups[current_idx] = idx
        current_idx = idx

    cups[current_idx] = initial_cups[0]
    current_idx = cups[current_idx]

    for _ in range(rounds):
        a = cups[current_idx]
        b = cups[a]
        c = cups[b]

        dest = current_idx - 1 if current_idx > 1 else max_cup

        while dest in (a, b, c):
            dest = dest - 1 if dest > 1 else max_cup

        cups[current_idx] = cups[c]
        cups[c] = cups[dest]
        cups[dest] = a

        current_idx = cups[current_idx]

    cups_ordered: Deque[int] = deque()
    current_idx = cups[1]

    while current_idx != 1:
        cups_ordered.append(current_idx)
        current_idx = cups[current_idx]

    return list(cups_ordered)


def p_1(input_file: IO,
        debug=False):  # pylint: disable=unused-argument
    initial_cups = parse(input_file)
    cups = play_game(initial_cups, len(initial_cups), 100)
    return ''.join(str(x) for x in cups)


def p_2(input_file: IO,
        debug=False):  # pylint: disable=unused-argument
    cups = play_game(parse(input_file), 10**6, 10**7)
    a, b = cups[:2]
    return a*b
