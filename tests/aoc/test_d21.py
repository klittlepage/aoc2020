import aoc.d21

from tests.aoc.test_base import BaseTestCase


class TestAll(BaseTestCase):
    def test_part_one(self):
        self.run_aoc_part(21, 2614, aoc.d21.p_1)

    def test_part_two(self):
        self.run_aoc_part(21, 'qhvz,kbcpn,fzsl,mjzrj,bmj,mksmf,gptv,kgkrhg',
                          aoc.d21.p_2)
