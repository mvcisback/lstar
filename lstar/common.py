from functools import wraps
from typing import TypeVar, Hashable, FrozenSet, Callable, Union

import funcy as fn
from dfa import DFA
from lazytree import LazyTree


Letter = Hashable
Alphabet = FrozenSet[Letter]

Word = TypeVar('Word')  # Tuple of elements of Alphabet.

LabelOracle = Callable[[Word], Letter]

CounterExample = Union[None, Word]
EquivalenceOracle = Callable[[DFA], CounterExample]


def validate_ce(labeler, retry=True):
    def _validate(find_ce):
        @wraps
        def _find_ce(cand):
            while True:
                word = find_ce(cand)
                if word is None:
                    return
                elif labeler(word) == cand.accepts(word):
                    return word
                elif not retry:
                    raise RuntimeError("Counter Example is invalid!")
        return _find_ce
    return _validate


def iterative_deeping_ce(labeler: LabelOracle, depth=10):
    def _iddfs(dfa: DFA) -> CounterExample:
        nodes = LazyTree(
            root=(),
            child_map=lambda w: [w + (i,) for i in dfa.inputs],
        ).iddfs(max_depth=depth)

        return fn.first(filter(lambda x: labeler(x) != dfa.label(x), nodes))
    return _iddfs
