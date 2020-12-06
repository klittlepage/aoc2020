import aoc.d06

from tests.aoc.test_base import BaseTestCase


class TestAll(BaseTestCase):
    def test_part_one(self):
        self.run_aoc_part(6, 6947, aoc.d06.p_1)

    def test_part_two(self):
        self.run_aoc_part(6, 3398, aoc.d06.p_2)
