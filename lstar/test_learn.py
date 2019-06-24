from lstar.learn import _learn_dfa, learn_dfa


def test_learn():
    count = 0

    def find_ce(_):
        nonlocal count
        assert count < 5
        count += 1
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
