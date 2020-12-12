import aoc.d11

from tests.aoc.test_base import BaseTestCase


class TestAll(BaseTestCase):
    def test_part_one(self):
        self.run_aoc_part(11, 2178, aoc.d11.p_1)

    def test_part_two(self):
        self.run_aoc_part(11, 1978, aoc.d11.p_2)
