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


def learn_dfa(inputs, label, find_counter_example, outputs=None) -> DFA:
    return fn.last(_learn_dfa(inputs, label, find_counter_example, outputs))


def _learn_dfa(inputs, label, find_ce, outputs=None, *, with_tree=False):
    """Generator API for learning DFA.

    Mainly useful for debugging.
    """
    learner = dfa_learner(inputs, label, outputs, with_tree=with_tree)
    hypothesis = next(learner)
    while True:
        yield hypothesis
        ce = find_ce(hypothesis)
        if ce is None:
            return
        hypothesis = learner.send(ce)


def dfa_learner(inputs, label, outputs=None, *, with_tree=False):
    """Co-routine API for learning DFA.

    Useful when learning multiple MAT theories simultaneously.
    """
    tree = ClassificationTree(
        labeler=label,
        outputs={True, False} if outputs is None else outputs,
    )

    while True:
        hypothesis = extract_dfa(tree, inputs)
        # DFA is lazily implemented.
        # Need to actually run through the DFA once to remove dependence
        # on membership oracle.
        hypothesis.states()
        ce = yield (hypothesis, tree) if with_tree else hypothesis
        tree.update_tree(ce, hypothesis)
