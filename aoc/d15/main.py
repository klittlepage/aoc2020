from typing import cast, Dict, IO, List, Optional, Tuple


def parse(input_file: IO) -> List[int]:
    return [int(x) for x in next(input_file).split(',')]


def run(numbers: List[int], turns: int) -> int:
    last_spoken = numbers[-1]
    spoken_age: Dict[int, Tuple[Optional[int], Optional[int]]] = \
        {number: (None, idx) for idx, number in enumerate(numbers)}

    for idx in range(len(numbers), turns):
        if last_spoken in spoken_age:
            n_1, n_2 = spoken_age[last_spoken]
            last_spoken = 0 if n_1 is None else cast(int, n_2) - cast(int, n_1)
            if last_spoken in spoken_age:
                n_1, n_2 = spoken_age[last_spoken]
                spoken_age[last_spoken] = (n_2, idx)
            else:
                spoken_age[last_spoken] = (None, idx)

    return last_spoken


def p_1(input_file: IO,
        debug=False):  # pylint: disable=unused-argument
    return run(parse(input_file), 2020)


def p_2(input_file: IO,
        debug=False):  # pylint: disable=unused-argument
    return run(parse(input_file), 30_000_000)
