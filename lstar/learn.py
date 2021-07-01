import funcy as fn
from dfa import DFA, dict2dfa, dfa2dict

from lstar.classification_tree import ClassificationTree
from lstar.common import Alphabet


def extract_dfa(tree: ClassificationTree, inputs: Alphabet) -> DFA:
    tmp_dfa = DFA(
        start=(),
        inputs=inputs,
        label=tree.labeler,
        transition=lambda w, c: tree.sift(w + (c,)).data,
        outputs=tree.outputs,
    )

    # Convert to dict (and back) to remove dependence on membership oracle.
    return dict2dfa(*dfa2dict(tmp_dfa))


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
        ce = yield (hypothesis, tree) if with_tree else hypothesis
        tree.update_tree(ce, hypothesis)
