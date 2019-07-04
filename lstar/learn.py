import funcy as fn
from dfa import DFA

from lstar.classification_tree import ClassificationTree
from lstar.common import Alphabet


def extract_dfa(tree: ClassificationTree, inputs: Alphabet) -> DFA:
    return DFA(
        start=(),
        inputs=inputs,
        label=tree.labeler,
        transition=lambda w, c: tree.sift(w + (c,)).data,
        outputs=tree.outputs,
    )


def learn_dfa(alphabet, membership, find_counter_example,
              lazy=False, outputs=None) -> DFA:
    hypotheses = _learn_dfa(
        alphabet, membership, find_counter_example, lazy, outputs
    )
    return fn.last(hypotheses)


def _learn_dfa(alphabet, membership, find_counter_example,
               lazy=False, outputs=None, *, with_tree=False):
    tree = ClassificationTree(
        labeler=membership,
        outputs={True, False} if outputs is None else outputs,
    )

    while True:
        hypothesis = extract_dfa(tree, alphabet)
        if not lazy:
            # DFA is lazily implemented.
            # Need to actually run through the DFA once to remove dependence
            # on membership oracle.
            hypothesis.states()

        yield (hypothesis, tree) if with_tree else hypothesis
        ce = find_counter_example(hypothesis)
        if ce is None:
            return

        tree.update_tree(ce, hypothesis)
