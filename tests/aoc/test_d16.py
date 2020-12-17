import aoc.d16

from tests.aoc.test_base import BaseTestCase


class TestAll(BaseTestCase):
    def test_part_one(self):
        self.run_aoc_part(16, 25895, aoc.d16.p_1)

    def test_part_two(self):
        self.run_aoc_part(16, 5865723727753, aoc.d16.p_2)
