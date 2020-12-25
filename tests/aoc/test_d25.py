import aoc.d25

from tests.aoc.test_base import BaseTestCase


class TestAll(BaseTestCase):
    def test_part_one(self):
        self.run_aoc_part(25, 12181021, aoc.d25.p_1)
