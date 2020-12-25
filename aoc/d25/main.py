import math

from typing import IO, Optional, Tuple


def parse(input_file: IO) -> Tuple[int, int]:
    card = next(input_file).strip()
    door = next(input_file).strip()
    return int(card), int(door)


def baby_step_giant_step(g: int, h: int, p: int) -> Optional[int]:
    '''
    Solve for h = g^x mod p given a prime p.

    https://en.wikipedia.org/wiki/Baby-step_giant-step
    '''
    N = math.ceil(math.sqrt(p - 1))
    lookup_table = {pow(g, i, p): i for i in range(N)}
    c = pow(g, N * (p - 2), p)

    for j in range(N):
        y = (h * pow(c, j, p)) % p
        if y in lookup_table:
            return j * N + lookup_table[y]

    return None


def p_1(input_file: IO,
        debug=False):  # pylint: disable=unused-argument
    p = 20201227
    card, door = parse(input_file)
    res = baby_step_giant_step(7, door, p)
    assert res is not None
    return pow(card, res, p)


def p_2(_input_file: IO,
        debug=False):  # pylint: disable=unused-argument
    pass
