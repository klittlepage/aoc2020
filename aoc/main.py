import argparse
import importlib
import os
import sys


def main():
    def check_day(arg):
        value = int(arg)
        if not 1 <= value <= 25:
            raise ValueError
        return value

    def check_part(arg):
        value = int(arg)
        if value not in [1, 2]:
            raise ValueError
        return value

    parser = argparse.ArgumentParser(prog='aoc2020')
    parser.add_argument('--debug', help='print debug info', default=False,
                        action='store_true')
    parser.add_argument('day', help='aoc challenge day, e.g., 1, 2, ... 25',
                        type=check_day)
    parser.add_argument('part', help='aoc challenge part, i.e., 1, 2',
                        type=check_part)

    parsed_args = parser.parse_args()

    day = parsed_args.day
    day_formatted = f"{day:02d}"
    part = parsed_args.part

    target_module = f"aoc.d{day_formatted}"
    module = importlib.import_module(target_module)

    try:
        target_method = getattr(module, "p_{}".format(parsed_args.part))
    except AttributeError:
        print(f"__init__.py for module {target_module} must include p_{part}")
        sys.exit(1)

    cur_path = os.path.dirname(os.path.realpath(__file__))
    data_path = os.path.join(cur_path, '..', 'data', f"d{day_formatted}",
                             'input.txt')

    with open(data_path, 'r', encoding='utf8') as input_file:
        res = target_method(input_file, debug=parsed_args.debug)
        if res:
            print(f"solution to day {day}, part {part}: {res}")
        else:
            print('no solution found')
            sys.exit(1)
