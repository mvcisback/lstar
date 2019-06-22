from typing import Mapping, Union

import attr
import funcy as fn
from dfa import DFA

from lstar.common import Alphabet, MembershipOracle, Word


@attr.s(auto_attribs=True)
class Node:
    data: Word
    children: Mapping[Alphabet, Union[None, "Node"]] = attr.ib(factory=dict)

    @property
    def is_leaf(self):
        return len(self.children) == 0

    @property
    def left(self):
        # TODO: remove
        return self.children.get(False)

    @property
    def right(self):
        # TODO: remove
        return self.children.get(True)


@attr.s(frozen=True, auto_attribs=True)
class ClassificationTree:
    alphabet: Alphabet
    membership: MembershipOracle
    root: Node = Node(())

    def _sift(self, word):
        node = self.root
        while not node.is_leaf:
            yield node
            test = word + node.data
            node = node.right if self.membership(test) else node.left

        yield node

    def access_words(self):
        stack = [self.root]
        while stack:
            node = stack.pop()
            if node.is_leaf:
                yield node
            else:
                stack.extend([node.left, node.right])

    def sift(self, word) -> Node:
        return fn.last(self._sift(word))

    def lca(self, word1, word2) -> Word:
        """Least Common Ancestor."""
        trace = zip(self._sift(word1), self._sift(word2))
        common_ancestors = (n1 for (n1, n2) in trace if n1 == n2)
        return fn.last(common_ancestors).data

    def extract_dfa(self) -> DFA:
        return DFA(
            start=(),
            alphabet=self.alphabet,
            accept=self.membership,
            transition=lambda w, c: self.sift(w + (c,)).data,
        )

    def update_tree(self, word: Word, hypothesis: DFA):
        if self.root.is_leaf:
            assert self.root.data == ()
            init_label = self.membership(())
            self.root.children[init_label] = Node(())
            self.root.children[not init_label] = Node(word)
            return

        sifts = map(self.sift, prefixes(word))
        trace = hypothesis.trace(word)

        prefix_prev = s_tree_prev = None
        for prefix, s_tree, s_cnd in zip(prefixes(word), sifts, trace):
            if s_tree.data != s_cnd:
                break

            prefix_prev, s_tree_prev = prefix, s_tree

        assert s_tree.data != s_cnd

        # TODO: can this membership query be infered already
        # from counter example?
        # TODO: Only need to perform n-1 tests for moore machine.
        test = (prefix[-1],) + self.lca(s_tree.data, s_cnd)
        test_res = self.membership(s_tree_prev.data + test)

        s_tree_prev.children = {
            test_res: Node(s_tree_prev.data),
            (not test_res): Node(prefix_prev),
        }
        s_tree_prev.data = test


def prefixes(word):
    return (word[:i] for i in range(len(word) + 1))
