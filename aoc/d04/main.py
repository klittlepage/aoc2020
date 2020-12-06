import itertools as it
import re

from typing import cast, Dict, IO, Iterator, Tuple

import aoc.common as common

_REQUIRED_FIELDS = set(['byr', 'iyr', 'eyr', 'hgt', 'hcl', 'ecl', 'pid'])


def parse(input_file: IO) -> Iterator[Dict[str, str]]:
    yield from (dict(cast(Tuple[str, str], tuple(pair.split(':'))) for pair in
                     it.chain(*(line.split(' ') for line in chunk))) for
                chunk in common.read_chunked(input_file))


def fields_present(x: Dict[str, str]) -> bool:
    res = _REQUIRED_FIELDS - set(x.keys())
    return not res or res == set(['cid'])


def p_1(input_file: IO,
        debug=False):  # pylint: disable=unused-argument
    return sum((fields_present(x) for x in parse(input_file)))


def p_2(input_file: IO,
        debug=False):  # pylint: disable=unused-argument

    year_regex = re.compile(r"^[0-9]{4,4}$")
    height_regex = re.compile(r"^([0-9]{2,3})(in|cm)$")
    hair_regex = re.compile(r"^#[0-9a-f]{6,6}$")
    eye_regex = re.compile(r"^(amb|blu|brn|gry|grn|hzl|oth)$")
    pid_regex = re.compile(r"^[0-9]{9,9}$")

    # pylint: disable=too-many-return-statements
    def is_valid(x: Dict[str, str]) -> bool:
        if not (year_regex.match(x['byr']) and 1920 <= int(x['byr']) <= 2002):
            return False
        if not (year_regex.match(x['byr']) and 2010 <= int(x['iyr']) <= 2020):
            return False
        if not (year_regex.match(x['byr']) and 2020 <= int(x['eyr']) <= 2030):
            return False
        if not height_regex.match(x['hgt']):
            return False
        if x['hgt'].endswith('in') and not 59 <= int(x['hgt'][:-2]) <= 76:
            return False
        if x['hgt'].endswith('cm') and not 150 <= int(x['hgt'][:-2]) <= 193:
            return False
        if not hair_regex.match(x['hcl']):
            return False
        if not eye_regex.match(x['ecl']):
            return False
        if not pid_regex.match(x['pid']):
            return False
        return True

    return sum((is_valid(x) for x in parse(input_file) if fields_present(x)))
