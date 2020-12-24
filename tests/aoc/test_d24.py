import aoc.d24

from tests.aoc.test_base import BaseTestCase


class TestAll(BaseTestCase):
    def test_part_one(self):
        self.run_aoc_part(24, 275, aoc.d24.p_1)

    def test_part_two(self):
        self.run_aoc_part(24, 3537, aoc.d24.p_2)
