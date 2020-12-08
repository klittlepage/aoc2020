import aoc.d07

from tests.aoc.test_base import BaseTestCase


class TestAll(BaseTestCase):
    def test_part_one(self):
        self.run_aoc_part(7, 222, aoc.d07.p_1)

    def test_part_two(self):
        self.run_aoc_part(7, 13264, aoc.d07.p_2)
