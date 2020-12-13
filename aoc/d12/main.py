import dataclasses
import math
import re

from typing import cast, IO, Iterator, Tuple, Union

TInstruction = Tuple[str, int]


def parse(input_file: IO) -> Iterator[TInstruction]:
    regex = re.compile(r"(N|S|E|W|L|R|F)([0-9]+)")

    def parse_entry(instruction: str) -> TInstruction:
        match = regex.match(instruction)
        assert match is not None
        (action, value) = cast(Tuple[str, str], match.groups())
        return (action, int(value))

    yield from (parse_entry(x) for x in input_file)


@dataclasses.dataclass
class _ShipPt1:
    x: int = 0
    y: int = 0
    orientation: int = 0

    # pylint: disable=too-many-branches
    def move(self, instruction: TInstruction):
        (action, value) = instruction

        if action == 'N':
            self.y += value
        elif action == 'S':
            self.y -= value
        elif action == 'E':
            self.x += value
        elif action == 'W':
            self.x -= value
        elif action == 'L':
            self.orientation = (self.orientation+value) % 360
        elif action == 'R':
            self.orientation = (self.orientation-value) % 360
        elif action == 'F':
            if self.orientation == 0:
                self.x += value
            elif self.orientation == 90:
                self.y += value
            elif self.orientation == 180:
                self.x -= value
            elif self.orientation == 270:
                self.y -= value
            else:
                assert False, 'bad cardinal direction'
        else:
            assert False, 'bad instruction'

    def manhattan_distance(self):
        return abs(self.x) + abs(self.y)


@dataclasses.dataclass
class _ShipPt2:
    x: int = 0
    y: int = 0
    orientation: int = 0
    waypoint_x: int = 10
    waypoint_y: int = 1

    def move(self, instruction: TInstruction):
        (action, value) = instruction

        if action == 'N':
            self.waypoint_y += value
        elif action == 'S':
            self.waypoint_y -= value
        elif action == 'E':
            self.waypoint_x += value
        elif action == 'W':
            self.waypoint_x -= value
        elif action in ['L', 'R']:
            assert value in [0, 90, 180, 270]
            radians = (1 if action == 'L' else -1)*math.pi*value/180
            prev_x = self.waypoint_x
            prev_y = self.waypoint_y
            self.waypoint_x = round(prev_x*math.cos(radians) -
                                    prev_y*math.sin(radians))
            self.waypoint_y = round(prev_x*math.sin(radians) +
                                    prev_y*math.cos(radians))
        elif action == 'F':
            self.x += value*self.waypoint_x
            self.y += value*self.waypoint_y
        else:
            assert False, 'bad instruction'

    def manhattan_distance(self):
        return abs(self.x) + abs(self.y)


def run(input_file: IO, ship: Union[_ShipPt1, _ShipPt2]) -> int:
    for instruction in parse(input_file):
        ship.move(instruction)

    return ship.manhattan_distance()


def p_1(input_file: IO,
        debug=False):  # pylint: disable=unused-argument
    return run(input_file, _ShipPt1())


def p_2(input_file: IO,
        debug=False):  # pylint: disable=unused-argument
    return run(input_file, _ShipPt2())
