"""
Pratt parsing based off of:

https://matklad.github.io/2020/04/13/simple-but-powerful-pratt-parsing.html
"""

import dataclasses
import functools as ft
import itertools as it
import operator as op
import re

from collections import deque
from typing import cast, Callable, Deque, IO, List, Optional, Tuple, Union


TPrecedence = Callable[[str], Optional[Tuple[int, int]]]


@dataclasses.dataclass
class Token:
    pass


@dataclasses.dataclass
class Operator(Token):
    value: str


@dataclasses.dataclass
class Literal(Token):
    value: str


@dataclasses.dataclass
class Eof(Token):
    pass


class Lexer:
    _tokens: Deque[Token]

    def __init__(self, expr):
        is_number = re.compile(r"[0-9]")

        def map_token(x):
            return Literal(x) if is_number.match(x) else Operator(x)

        tokens = [map_token(x) for x in
                  it.filterfalse(lambda x: x.isspace(), expr)]
        self._tokens = deque(tokens)

    def peek(self) -> Token:
        if not self._tokens:
            return Eof()

        return self._tokens[0]

    def pop(self) -> Token:
        if not self._tokens:
            return Eof()

        return self._tokens.popleft()

    def __repr__(self):
        return str(self._tokens)

    def __str__(self):
        return repr(self)


@dataclasses.dataclass
class SExpr:
    def eval(self) -> int:  # pylint: disable=no-self-use
        raise Exception('bad eval')


@dataclasses.dataclass
class Atom(SExpr):
    value: str

    def eval(self) -> int:
        return int(self.value)

    def __repr__(self):
        return self.value

    def __str__(self):
        return repr(self)


@dataclasses.dataclass
class Cons(SExpr):
    value: str
    expr: List[SExpr]

    def eval(self) -> int:
        return ft.reduce(op.mul if self.value == '*' else op.add,
                         (x.eval() for x in self.expr))

    def __repr__(self):
        rest = " ".join([str(x) for x in self.expr])
        return f"({self.value} {rest})"


def expr_with_power(lexer: Lexer,
                    op_binding_power: TPrecedence,
                    min_binding_power: int) -> SExpr:
    token = lexer.pop()

    if isinstance(token, Literal):
        lhs: Union[str, SExpr] = Atom(token.value)
    elif isinstance(token, Operator) and token.value == '(':
        if token.value == '(':
            lhs = expr_with_power(lexer, op_binding_power, 0)
            next_token = lexer.pop()
            if not isinstance(next_token, Operator) and \
                    cast(Operator, next_token).value == ')':
                raise Exception("bad expression; unclosed paren")
    else:
        raise Exception(f"bad token {token}")

    while True:
        next_token = lexer.peek()

        if isinstance(next_token, Eof):
            break
        if isinstance(next_token, Operator):
            sexpr_op = next_token.value
        else:
            raise Exception(f"bad token {token}")

        binding_power = op_binding_power(sexpr_op)
        if not binding_power:
            break

        lhs_binding_power, rhs_binding_power = binding_power

        if lhs_binding_power < min_binding_power:
            break

        lexer.pop()

        rhs = expr_with_power(lexer, op_binding_power, rhs_binding_power)
        lhs = Cons(sexpr_op, cast(List[SExpr], [lhs, rhs]))

    return cast(SExpr, lhs)


def parse_expr(expr: str, op_binding_power: TPrecedence) -> SExpr:
    lexer = Lexer(expr)
    return expr_with_power(lexer, op_binding_power, 0)


def run(input_file: IO, op_binding_power: TPrecedence) -> int:
    return sum(parse_expr(line, op_binding_power).eval() for line in input_file)


def p_1(input_file: IO,
        debug=False):  # pylint: disable=unused-argument
    def op_binding_power(sexpr_op: str) -> Optional[Tuple[int, int]]:
        return (1, 2) if sexpr_op in ['+', '*'] else None

    return run(input_file, op_binding_power)


def p_2(input_file: IO,
        debug=False):  # pylint: disable=unused-argument
    def op_binding_power(sexpr_op: str) -> Optional[Tuple[int, int]]:
        if sexpr_op == '*':
            return (1, 2)
        if sexpr_op == '+':
            return (3, 4)
        return None

    return run(input_file, op_binding_power)
