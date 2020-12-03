import aoc.d03

from tests.aoc.test_base import BaseTestCase


class TestAll(BaseTestCase):
    def test_part_one(self):
        self.run_aoc_part(3, 145, aoc.d03.p_1)

    def test_part_two(self):
        self.run_aoc_part(3, 3424528800, aoc.d03.p_2)
