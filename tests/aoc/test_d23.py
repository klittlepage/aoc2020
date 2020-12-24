import aoc.d23

from tests.aoc.test_base import BaseTestCase


class TestAll(BaseTestCase):
    def test_part_one(self):
        self.run_aoc_part(23, '35827964', aoc.d23.p_1)

    def test_part_two(self):
        self.run_aoc_part(23, 5403610688, aoc.d23.p_2)
