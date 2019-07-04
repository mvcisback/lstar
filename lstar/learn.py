import funcy as fn
from dfa import DFA

from lstar.classification_tree import ClassificationTree


def extract_dfa(tree: ClassificationTree) -> DFA:
    return DFA(
        start=(),
        inputs=tree.alphabet,
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
               lazy=False, outputs=None):
    tree = ClassificationTree(
        alphabet=alphabet,
        labeler=membership,
        outputs={True, False} if outputs is None else outputs,
    )

    while True:
        hypothesis = extract_dfa(tree)
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
