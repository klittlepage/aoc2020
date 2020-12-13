import functools as ft
import itertools as it
import math as ma
import operator as op

from typing import IO, List, Optional, Tuple


def parse(input_file: IO) -> Tuple[int, List[Optional[int]]]:
    earliest = int(next(input_file))
    bus_ids = [int(x) if x != 'x' else None for x in
               next(input_file).split(',')]
    return (earliest, bus_ids)


def egcd(a: int, b: int) -> Tuple[int, int, int]:
    if a == 0:
        return (b, 0, 1)

    g, y, x = egcd(b % a, a)
    return (g, x - (b // a) * y, y)


def modinv(a: int, m: int) -> int:
    g, x, _ = egcd(a, m)
    if g != 1:
        raise Exception('modular inverse does not exist')
    return x % m


def p_1(input_file: IO,
        debug=False):  # pylint: disable=unused-argument
    def first_time_after(earliest: int, bus_id: int) -> int:
        multiple, remainder = divmod(earliest, bus_id)
        return earliest if remainder == 0 else (multiple+1)*bus_id

    earliest, bus_ids = parse(input_file)
    arrival_time, best_bus_id = \
        min(((first_time_after(earliest, bus_id), bus_id) for
             bus_id in bus_ids if bus_id is not None), key=op.itemgetter(0))
    return (arrival_time-earliest)*best_bus_id


def p_2(input_file: IO,
        debug=False):  # pylint: disable=unused-argument
    # pylint: disable=anomalous-backslash-in-string
    """
    Solution via the Chinese remainder theorem.

    Taking the example:

    7,13,x,x,59,x,31,19

    We note that t must be a number s.t.

    t ≡ 0 (mod 7)
    t + 1 ≡ 0 (mod 13)
    t + 4 ≡ 0 (mod 59)
    t + 6 ≡ 0 (mod 31)
    t + 7 ≡ 0 (mod 19)

    We can re-write this in the form:

    t ≡ 0 (mod 7)
    t ≡ 12 (mod 13)
    t ≡ 55 (mod 59)
    t ≡ 25 (mod 31)
    t ≡ 12 (mod 19)

    This is the canonical form for a system of simultaneous congruencies:

    x ≡ a_1 (mod n_1)
    x ≡ a_2 (mod n_2)
      .
      .
    x ≡ a_k (mod n_k)

    Provided that n_1 \ldots n_k are pairwise coprime positive integers, it
    follows that a unique solution modulo N = (n_1\cdot n_2\cdots n_k) exists,
    and that we can find it using the Chinese Remainder Theorem:

    https://brilliant.org/wiki/chinese-remainder-theorem/
    """

    _earliest, bus_ids = parse(input_file)
    assert all(ma.gcd(*x) == 1 for x in
               it.combinations((x for x in bus_ids if x is not None), 2)), \
        'moduli are not pairwise coprime as required by the CRM'

    n = [x for x in bus_ids if x is not None]
    a = [ma.ceil(idx/bus_id)*bus_id-idx for idx, bus_id in
         enumerate(bus_ids) if bus_id is not None]
    N = ft.reduce(op.mul, n)
    y = [N//n_i for n_i in n]
    z = [modinv(y_i, n_i) for y_i, n_i in zip(y, n)]
    return sum(a_i*y_i*z_i for a_i, y_i, z_i in zip(a, y, z)) % N
