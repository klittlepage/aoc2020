from typing import IO, List, Tuple

import aoc.common.vm as vm


def _run_until_cycle(instructions: List[vm.Instruction]) -> Tuple[bool, int]:
    state = vm.State()
    trace = set()
    while state.pc < len(instructions):
        if state.pc in trace:
            return (False, state.acc)

        trace.add(state.pc)
        state = vm.step(instructions[state.pc], state)

    return (True, state.acc)


def p_1(input_file: IO,
        debug=False):  # pylint: disable=unused-argument
    return _run_until_cycle(vm.parse(input_file))[1]


def p_2(input_file: IO,
        debug=False):  # pylint: disable=unused-argument
    instructions = vm.parse(input_file)

    def flip(inst: vm.Instruction) -> vm.Instruction:
        if inst.op_code == vm.OpCode.NOP:
            return vm.Instruction(vm.OpCode.JMP, inst.value)
        if inst.op_code == vm.OpCode.JMP:
            return vm.Instruction(vm.OpCode.NOP, inst.value)
        return inst

    for mutation_idx, _ in enumerate(instructions):
        mutated = [instructions[idx] if idx != mutation_idx else flip(inst)
                   for idx, inst in enumerate(instructions)]

        terminated, acc = _run_until_cycle(mutated)
        if terminated:
            return acc
