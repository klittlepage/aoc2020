import aoc.d13

from tests.aoc.test_base import BaseTestCase


class TestAll(BaseTestCase):
    def test_part_one(self):
        self.run_aoc_part(13, 171, aoc.d13.p_1)

    def test_part_two(self):
        self.run_aoc_part(13, 539746751134958, aoc.d13.p_2)
