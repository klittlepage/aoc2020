from typing import Callable, Iterator, Tuple, TypeVar

T = TypeVar('T')
V = TypeVar('V')


def backtracking(reject: Callable[[T, V], bool],
                 accept: Callable[[T, V], bool],
                 next_candidate: Callable[[T, V], Iterator[Tuple[T, V]]],
                 starting_state: T,
                 first_candidate: V) -> Iterator[V]:

    def _helper(state: T, candidate: V) -> Iterator[V]:
        if reject(state, candidate):
            return

        if accept(state, candidate):
            yield candidate

        for (new_state, new_candidate) in next_candidate(state, candidate):
            yield from _helper(new_state, new_candidate)

    yield from _helper(starting_state, first_candidate)
