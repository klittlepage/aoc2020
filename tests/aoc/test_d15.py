import aoc.d15

from tests.aoc.test_base import BaseTestCase


class TestAll(BaseTestCase):
    def test_part_one(self):
        self.run_aoc_part(15, 929, aoc.d15.p_1)

    def test_part_two(self):
        self.run_aoc_part(15, 16671510, aoc.d15.p_2)
