import funcy as fn
from dfa import DFA

from lstar.classification_tree import ClassificationTree


def learn_dfa(alphabet, membership, find_counter_example, lazy=False) -> DFA:
    hypotheses = _learn_dfa(alphabet, membership, find_counter_example, lazy)
    return fn.last(hypotheses)


def _learn_dfa(alphabet, membership, find_counter_example, lazy=False):
    tree = ClassificationTree(
        alphabet=alphabet,
        membership=membership,
    )

    while True:
        hypothesis = tree.extract_dfa()
        if not lazy:
            # DFA is lazily implemented.
            # Need to actually run through the DFA once to remove dependence
            # on membership oracle.
            hypothesis.states()

        yield hypothesis
        ce = find_counter_example(hypothesis)
        if ce is None:
            return

        tree.update_tree(ce, hypothesis)
