from typing import TypeVar, Hashable, FrozenSet, Callable, Union

import attr
import funcy as fn
from dfa import DFA


Letter = Hashable
Alphabet = FrozenSet[Hashable]
Word = TypeVar('Word')  # Hashable Sequence of elements of Alphabet.

MembershipOracle = Callable[[Word], bool]

CounterExample = Union[bool, Word]
EquivalenceOracle = Callable[[Word], CounterExample]


@attr.s(auto_attribs=True)
class Node:
    distinguishing: Word
    left: Union[Word, "Node"]  # Fixed in python 3.7
    right: Union[Word, "Node"]


@attr.s(frozen=True, auto_attribs=True)
class ClassificationTree:
    membership: MembershipOracle
    equivalence: EquivalenceOracle
    alphabet: FrozenSet[Letter]
    root: Node

    def _sift(self, word):
        node = self.root
        while isinstance(node, Node):
            yield node.distinguishing

            if self.membership(word + node.distinguishing):
                node = node.right
            else:
                node = node.left

        yield node

    def _leaves(self):
        stack = [self.root]
        while stack:
            node = stack.pop()
            if isinstance(node, Node):
                stack.extend([node.left, node.right])
            else:
                yield node

    def sift(self, word) -> Word:
        return fn.last(self._sift(word))

    def lca(self, word1, word2) -> Word:
        """Least Common Ancestor."""
        trace = zip(self._sift(word1), self._sift(word2))
        common_ancestors = ((n1, n2) for (n1, n2) in trace if n1 == n2)
        return fn.last(common_ancestors)

    def extract_dfa(self) -> DFA:
        start=self.root.distinguishing if isinstance(self.root, Node) else node
        return DFA(
            start=start,
            alphabet=self.alphabet,
            accept=self.membership,
            transition=self.sift,
        )
