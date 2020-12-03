#!/bin/bash

DAY=$(printf "d%02d" $1)
MODULE=aoc/$DAY
mkdir -p $MODULE
mkdir -p data/$DAY/1
mkdir -p data/$DAY/2

cat << EOF > $MODULE/__init__.py
from aoc.$DAY.main import p_1, p_2
EOF

cat << EOF > $MODULE/main.py
from typing import IO

def p_1(input_file: IO, debug=False):
    pass

def p_2(input_file: IO, debug=False):
    pass
EOF

cat << EOF > tests/aoc/test_$DAY.py
import aoc.$DAY

from tests.aoc.test_base import BaseTestCase


class TestAll(BaseTestCase):
    def test_part_one(self):
        self.run_aoc_part($1, 1, False, aoc.$DAY.p_1)

    def test_part_two(self):
        self.run_aoc_part($1, 2, False, aoc.$DAY.p_2)
EOF
