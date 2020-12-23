from collections import deque

import functools as ft
import itertools as it

from typing import Deque, IO, Tuple


def parse(input_file: IO) -> Tuple[Deque[int], Deque[int]]:
    all_lines = input_file.read().strip().split('\n')
    player_1 = list(it.takewhile(lambda x: x != '', all_lines))[1:]
    player_2 = list(it.dropwhile(lambda x: x != 'Player 2:', all_lines))[1:]
    return deque(int(x) for x in player_1), deque(int(x) for x in player_2)


def compute_score(winning_deck: Deque[int]) -> int:
    return ft.reduce(lambda acc, x: acc+x[0]*x[1],
                     zip(reversed(winning_deck), it.count(1)), 0)


def p_1(input_file: IO,
        debug=False):  # pylint: disable=unused-argument
    player_1, player_2 = parse(input_file)

    while player_1 and player_2:
        p_1_top = player_1.popleft()
        p_2_top = player_2.popleft()

        if p_1_top > p_2_top:
            player_1.extend([p_1_top, p_2_top])
        else:
            player_2.extend([p_2_top, p_1_top])

    return compute_score(player_1 if player_1 else player_2)


def p_2(input_file: IO,
        debug=False):  # pylint: disable=unused-argument
    def play_game(player_1: Deque[int], player_2: Deque[int]) -> bool:
        prev_decks = set()

        while player_1 and player_2:
            game_key = (tuple(player_1), tuple(player_2))
            if game_key in prev_decks:
                return True
            prev_decks.add(game_key)

            p_1_top = player_1.popleft()
            p_2_top = player_2.popleft()

            if len(player_1) >= p_1_top and len(player_2) >= p_2_top:
                p_1_win = play_game(deque(list(player_1)[:p_1_top]),
                                    deque(list(player_2)[:p_2_top]))
            else:
                p_1_win = p_1_top > p_2_top

            if p_1_win:
                player_1.extend([p_1_top, p_2_top])
            else:
                player_2.extend([p_2_top, p_1_top])

        return bool(player_1)

    player_1, player_2 = parse(input_file)
    play_game(player_1, player_2)
    return compute_score(player_1 if player_1 else player_2)
