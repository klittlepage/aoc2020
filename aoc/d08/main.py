import copy
import re

from dataclasses import dataclass
from enum import Enum, auto
from typing import cast, List, IO, Tuple


class OpCode(Enum):
    NOP = auto()
    ACC = auto()
    JMP = auto()


_OPCODE_MAP = {
    'nop': OpCode.NOP,
    'acc': OpCode.ACC,
    'jmp': OpCode.JMP
}


@dataclass
class Instruction:
    op_code: OpCode
    value: int


@dataclass
class State:
    pc: int = 0
    acc: int = 0


def parse(lines: IO) -> List[Instruction]:
    instruction_regex = re.compile(r"(nop|acc|jmp)\s((\+|-)[0-9]+)")

    def _parse_instruction(line: str) -> Instruction:
        match = instruction_regex.match(line)
        assert match is not None
        op_code, value, _ = cast(Tuple[str, str, str], match.groups())
        return Instruction(_OPCODE_MAP[op_code], int(value))
    return [_parse_instruction(line) for line in lines]


def _nop(_value: int, state: State) -> State:
    state.pc += 1
    return state


def _acc(value: int, state: State) -> State:
    state.pc += 1
    state.acc += value
    return state


def _jmp(value: int, state: State) -> State:
    state.pc += value
    return state


_DISPATCHER = {
    OpCode.NOP: _nop,
    OpCode.ACC: _acc,
    OpCode.JMP: _jmp,
}


def step(instruction: Instruction, state: State) -> State:
    return _DISPATCHER[instruction.op_code](instruction.value,
                                            copy.deepcopy(state))


def run(instructions: List[Instruction]) -> State:
    state = State()
    while state.pc < len(instructions):
        state = step(instructions[state.pc], copy.deepcopy(state))

    return state


def _run_until_cycle(instructions: List[Instruction]) -> Tuple[bool, int]:
    state = State()
    trace = set()
    while state.pc < len(instructions):
        if state.pc in trace:
            return (False, state.acc)

        trace.add(state.pc)
        state = step(instructions[state.pc], state)

    return (True, state.acc)


def p_1(input_file: IO,
        debug=False):  # pylint: disable=unused-argument
    return _run_until_cycle(parse(input_file))[1]


def p_2(input_file: IO,
        debug=False):  # pylint: disable=unused-argument
    instructions = parse(input_file)

    def flip(inst: Instruction) -> Instruction:
        if inst.op_code == OpCode.NOP:
            return Instruction(OpCode.JMP, inst.value)
        if inst.op_code == OpCode.JMP:
            return Instruction(OpCode.NOP, inst.value)
        return inst

    for mutation_idx, _ in enumerate(instructions):
        mutated = [instructions[idx] if idx != mutation_idx else flip(inst)
                   for idx, inst in enumerate(instructions)]

        terminated, acc = _run_until_cycle(mutated)
        if terminated:
            return acc
