from lstar.learn import _learn_dfa


def test_learn():
    count = 0

    def find_counter_example(_):
        nonlocal count
        assert count < 5
        count += 1
        if count < 4:
            return (1, 1, 0, 1)
        elif count >= 4:
            return None

    def membership(state):
        return sum(state) % 4 == 3

    hypotheses = _learn_dfa({0, 1}, membership, find_counter_example)
    for i, dfa in enumerate(hypotheses):
        assert i < 4
        if i < 3:
            assert len(dfa.states()) == 1
            assert not dfa.accepts((1, 1, 0, 1))
        else:
            assert len(dfa.states()) == 4
            assert dfa.accepts((1, 1, 0, 1))

    # TODO: implement actual DFA equivalence checking.
