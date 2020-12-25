from typing import IO, Tuple


def parse(input_file: IO) -> Tuple[int, int]:
    card = next(input_file).strip()
    door = next(input_file).strip()
    return int(card), int(door)


def p_1(input_file: IO,
        debug=False):  # pylint: disable=unused-argument
    card, door = parse(input_file)

    e = 0
    n = 1
    while n != door:
        e += 1
        n = 7*n % 20201227

    return pow(card, e, 20201227)


def p_2(_input_file: IO,
        debug=False):  # pylint: disable=unused-argument
    pass
