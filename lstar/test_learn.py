from lstar.learn import _learn_dfa, learn_dfa


def test_learn_dfa():
    def find_ce(dfa):
        count = len(dfa.states())
        if count < 4:
            return (1, 1, 0, 1)
        elif count >= 4:
            return None

    def membership(state):
        return sum(state) % 4 == 3

    hypotheses = _learn_dfa({0, 1}, membership, find_ce)
    for i, dfa in enumerate(hypotheses):
        assert i < 4
        if i < 3:
            assert len(dfa.states()) == 1
            assert not dfa.label((1, 1, 0, 1))
        else:
            assert len(dfa.states()) == 4
            assert dfa.label((1, 1, 0, 1))

    assert learn_dfa({0, 1}, membership, find_ce).label((1, 1, 0, 1))

    # TODO: implement actual DFA equivalence checking.


def test_learn_moore1():
    def label(word):
        count = sum(word)
        if count == 0:
            return 0
        count -= 1
        return (count % 2) + 1

    def ce(dfa):
        # assert len(dfa.states()) <= 3
        return (1,) if len(dfa.states()) < 3 else None

    assert label(()) == 0
    assert label((1, )) == 1
    assert label((0, )) == 0
    dfa = learn_dfa(
        alphabet={0, 1},
        membership=label,
        find_counter_example=ce,
        outputs={0, 1, 2},
    )
    assert dfa.label(()) == 0
    assert dfa.label((1,)) == 1
    assert dfa.label((1, 1)) == 2
    assert dfa.label((1, 1, 1)) == 1
    assert dfa.label((1, 0, 1)) == 2
    assert dfa.label((0, 1)) == 1
    assert dfa.label((0,)) == 0


def test_learn_moore2():
    def find_ce(dfa):
        count = len(dfa.states())
        assert count in (1, 4)
        if count < 4:
            return (1, 1, 0, 1)
        elif count >= 4:
            return None

    def label(state):
        return sum(state) % 4

    assert label(()) == 0
    assert label((1,)) == 1
    assert label((1, 1, )) == 2
    assert label((1, 1, 1)) == 3
    assert label((1, 1, 0, 1)) == 3
    assert label((1, 1, 1, 1)) == 0

    dfl = learn_dfa(
        alphabet={0, 1},
        membership=label,
        find_counter_example=find_ce,
        outputs={0, 1, 2},
    )

    assert dfl.transduce(()) == ()
    assert dfl.transduce((1,)) == (0,)
    assert dfl.transduce((1, 1, )) == (0, 1)
    assert dfl.transduce((1, 1, 1)) == (0, 1, 2)
    assert dfl.transduce((1, 1, 0, 1)) == (0, 1, 2, 2)
    assert dfl.transduce((1, 1, 1, 1, 1)) == (0, 1, 2, 3, 0)
