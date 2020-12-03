from typing import IO, List, Optional, Tuple


def parse(input_file: IO) -> List[int]:
    return [int(x) for x in input_file.readlines()]


def sum_to(input_list: List[int], target: int) -> Optional[Tuple[int, int]]:
    l = 0
    r = len(input_list) - 1
    while l < r:
        v_l = input_list[l]
        v_r = input_list[r]
        test_sum = v_l + v_r
        if test_sum == target:
            return v_l, v_r
        if test_sum < target:
            l += 1
        else:
            r -= 1
    return None


def p_1(input_file: IO, debug=False):
    res = sum_to(sorted(parse(input_file)), 2020)
    if res:
        x, y = res
        solution = x*y
        if debug:
            print(f"{x} + {y} = {x+y}, {x} * {y} = {solution}")
        return solution

    return None


def p_2(input_file: IO, debug=False):
    sorted_list = sorted(parse(input_file))

    for v_1 in sorted_list:
        res = sum_to(sorted_list, 2020-v_1)
        if res:
            v_2, v_3 = res
            solution = v_1*v_2*v_3
            if debug:
                print(f"{v_1} + {v_2} + {v_3} = {v_1+v_2+v_3}, "
                      f"{v_1} * {v_2} * {v_3} = {v_1*v_2*v_3}")
            return solution

    return None
