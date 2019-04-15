from typing import TypeVar, Hashable, FrozenSet, Callable, Union

from dfa import DFA


Letter = Hashable
Alphabet = FrozenSet[Letter]
Word = TypeVar('Word')  # Tuple of elements of Alphabet.

MembershipOracle = Callable[[Word], bool]

CounterExample = Union[None, Word]
EquivalenceOracle = Callable[[DFA], CounterExample]
