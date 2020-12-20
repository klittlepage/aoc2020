import aoc.d19

from tests.aoc.test_base import BaseTestCase


class TestAll(BaseTestCase):
    def test_part_one(self):
        self.run_aoc_part(19, 208, aoc.d19.p_1)

    def test_part_two(self):
        self.run_aoc_part(19, 316, aoc.d19.p_2)
