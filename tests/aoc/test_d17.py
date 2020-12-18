import aoc.d17

from tests.aoc.test_base import BaseTestCase


class TestAll(BaseTestCase):
    def test_part_one(self):
        self.run_aoc_part(17, 218, aoc.d17.p_1)

    def test_part_two(self):
        self.run_aoc_part(17, 1908, aoc.d17.p_2)
