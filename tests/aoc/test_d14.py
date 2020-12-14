import aoc.d14

from tests.aoc.test_base import BaseTestCase


class TestAll(BaseTestCase):
    def test_part_one(self):
        self.run_aoc_part(14, 5902420735773, aoc.d14.p_1)

    def test_part_two(self):
        self.run_aoc_part(14, 3801988250775, aoc.d14.p_2)
