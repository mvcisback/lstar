from lstar.classification_tree import ClassificationTree

from dfa import DFA


def learn_dfa(alphabet, membership, find_counter_example) -> DFA:
    tree = ClassificationTree(
        alphabet=alphabet,
        membership=membership,
    )
    
    while True:
        hypothesis = tree.extract_dfa()
        ce = find_counter_example(hypothesis)
        if ce is None:
            return hypothesis
        
        tree.update_tree(ce, hypothesis)
