import unittest
import os


class BaseTestCase(unittest.TestCase):
    @staticmethod
    def get_path(day, part):
        cur_path = os.path.dirname(os.path.realpath(__file__))
        return os.path.join(cur_path, '../../', 'data', f"d{day:02d}",
                            str(part), 'input.txt')

    def run_aoc_part(self, day, part, expected, method):
        with open(BaseTestCase.get_path(day, part), 'r',
                  encoding='utf8') as input_file:
            self.assertEqual(expected, method(input_file))
