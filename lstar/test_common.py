from lstar.common import iterative_deeping_ce
from lstar.learn import learn_dfa


def test_iddfs_ce():
    def membership(word):
        return sum(word) % 4 == 3

    find_ce = iterative_deeping_ce(membership)

    dfa = learn_dfa({0, 1}, membership, find_ce)
    assert dfa.label((1, 1, 0, 1))
