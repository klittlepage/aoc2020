import re

import functools as ft

from typing import Any, cast, Dict, IO, Iterator, List, Tuple

TInstBlock = Tuple[str, List[Tuple[int, int]]]


def parse(input_file: IO) -> Iterator[TInstBlock]:
    mask = re.compile(r"^mask = (\w+)$")
    mem = re.compile(r"^mem\[([0-9]+)\] = ([0-9]+)$")

    cur_mask = None
    block: List[Tuple[int, int]] = list()
    for line in input_file:
        mask_match = mask.match(line)
        if mask_match:
            if cur_mask is not None:
                yield (cur_mask, block)
            cur_mask = mask_match.group(1)
            block = list()
        else:
            mem_match = mem.match(line)
            assert mem_match is not None
            block.append((int(mem_match.group(1)), int(mem_match.group(2))))

    if cur_mask and block:
        yield (cur_mask, block)


def value_to_bin(x: int) -> str:
    return bin(x)[2:].zfill(36)


def p_1(input_file: IO,
        debug=False):  # pylint: disable=unused-argument
    def block_reducer(acc: Dict[int, int],
                      x: Tuple[int, int],
                      mask: str) -> Dict[int, int]:
        address, value = x
        acc[address] = int(''.join(v if m == 'X' else m for v, m in
                                   zip(value_to_bin(value), mask)), 2)
        return acc

    def reducer(acc: Dict[int, int], x: TInstBlock) -> Dict[int, int]:
        mask, instructions = x
        return ft.reduce(lambda acc, x: block_reducer(acc, x, mask),
                         instructions, acc)

    return sum(ft.reduce(reducer, parse(input_file),
                         cast(Dict[Any, Any], dict())).values())


def p_2(input_file: IO,
        debug=False):  # pylint: disable=unused-argument
    def expand_mask(mask: str, address: int) -> Iterator[int]:
        def helper(x: str) -> Iterator[str]:
            if x == '':
                yield ''
            elif x[0] == 'X':
                yield from ('0' + c for c in helper(x[1:]))
                yield from ('1' + c for c in helper(x[1:]))
            else:
                yield from (x[0] + c for c in helper(x[1:]))

        masked = ''.join(v if m == '0' else m for v, m in
                         zip(value_to_bin(address), mask))
        yield from (int(x, 2) for x in helper(masked))

    memory = dict()
    for (mask, instructions) in parse(input_file):
        for (address, value) in instructions:
            for masked_address in expand_mask(mask, address):
                memory[masked_address] = value

    return sum(memory.values())
