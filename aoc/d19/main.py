import dataclasses
import re

from collections import deque
from typing import cast, Dict, IO, List, Tuple


@dataclasses.dataclass
class BaseRule:
    pass


@dataclasses.dataclass
class Terminal(BaseRule):
    value: str


@dataclasses.dataclass
class MatchRule(BaseRule):
    rule_groups: List[List[int]]


TRules = Dict[int, BaseRule]


def parse(input_file: IO) -> Tuple[TRules, List[str]]:
    expr = re.compile(r"^([0-9]+): (.+)")
    rules: TRules = dict()

    for line in input_file:
        if line.isspace():
            break

        match = expr.match(line.strip())
        assert match is not None

        rule_no = int(match.group(1))
        rule_groups = list()
        rule_group: List[int] = list()

        lexbuff = deque(match.group(2))
        while lexbuff:
            if lexbuff[0] == '"':
                lexbuff.popleft()
                rules[rule_no] = Terminal(lexbuff.popleft())
                if not lexbuff.popleft() == '"':
                    raise Exception('terminal missing terminating quote')
                if lexbuff:
                    raise Exception(
                        'parse did not consume buffer for terminal')
            elif lexbuff[0] == ' ':
                lexbuff.popleft()
            elif lexbuff[0] == '|':
                lexbuff.popleft()
                rule_groups.append(rule_group)
                rule_group = list()
            elif ord('0') <= ord(lexbuff[0]) <= ord('9'):
                int_str = ''
                while lexbuff and ord('0') <= ord(lexbuff[0]) <= ord('9'):
                    int_str += lexbuff.popleft()
                rule_group.append(int(int_str))
            else:
                raise Exception('bad parse')

        if rule_group:
            rule_groups.append(rule_group)
            rules[rule_no] = MatchRule(rule_groups)

    messages = [x.strip() for x in input_file]

    return rules, messages


def eval_rule(rules: TRules,
              rule_numbers: List[int],
              message: str) -> bool:
    if not rule_numbers or message == '':
        return not rule_numbers and message == ''

    active_rule = rules[rule_numbers[0]]

    if isinstance(active_rule, Terminal):
        return eval_rule(rules, rule_numbers[1:], message[1:]) if \
            message[0] == cast(Terminal, active_rule).value else False

    return any(eval_rule(rules, left + rule_numbers[1:], message) for
               left in cast(MatchRule, active_rule).rule_groups)


def run(rules: TRules, messages: List[str]) -> int:
    return sum(eval_rule(rules, [0], message) for message in messages)


def p_1(input_file: IO,
        debug=False):  # pylint: disable=unused-argument
    return run(*parse(input_file))


def p_2(input_file: IO,
        debug=False):  # pylint: disable=unused-argument
    rules, messages = parse(input_file)
    rules[8] = MatchRule([[42], [42, 8]])
    rules[11] = MatchRule([[42, 31], [42, 11, 31]])
    return run(rules, messages)
