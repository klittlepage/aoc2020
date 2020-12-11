import aoc.d09

from tests.aoc.test_base import BaseTestCase


class TestAll(BaseTestCase):
    def test_part_one(self):
        self.run_aoc_part(9, 373803594, aoc.d09.p_1)

    def test_part_two(self):
        self.run_aoc_part(9, 51152360, aoc.d09.p_2)
