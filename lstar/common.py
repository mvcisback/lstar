from functools import wraps
from typing import TypeVar, Hashable, FrozenSet, Callable, Union

from dfa import DFA


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
