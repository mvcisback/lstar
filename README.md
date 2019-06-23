# L*

[![Build Status](https://travis-ci.com/mvcisback/lstar.svg?branch=master)](https://travis-ci.com/mvcisback/lstar)
[![codecov](https://codecov.io/gh/mvcisback/DiscreteSignals/branch/master/graph/badge.svg)](https://codecov.io/gh/mvcisback/lstar)
[![PyPI version](https://badge.fury.io/py/lstar.svg)](https://badge.fury.io/py/lstar)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

Implementation of the discriminant tree L* algorithm DFA learning algorithm
provided in [^1].

# Installation

If you just need to use `lstar`, you can just run:

`$ pip install lstar`

For developers, note that this project uses the
[poetry](https://poetry.eustace.io/) python package/dependency
management tool. Please familarize yourself with it and then
run:

`$ poetry install`

# Usage

```
from lstar import learn_dfa

def is3mod4(word):
    """Want to learn 4 state counter"""
    return sum(word) % 4 == 3


def ask_human(dfa):
    """User generated counter example.

    An alternative includes sampling or checking against an approximate
    model.
    """
    print(dfa)
    return tuple(input("> Please provide a counter example "))


dfa = learn_dfa(
    alphabet={0, 1},  #  Possible inputs.
    membership=is3mod4,  #  Does this sequence belong in the language.
    find_counter_example=ask_human,  #  Use a human for counter examples.
)

assert not dfa.accepts(())
assert not dfa.accepts((1,))
assert not dfa.accepts((1, 1, ))
assert dfa.accepts((1, 1, 1))
assert dfa.accepts((1, 1, 0, 1))
```

# Testing

This project uses pytest. Simply run

`$ pytest`

in the root of the repository.


[^1]: Kearns, Michael J., Umesh Virkumar Vazirani, and Umesh Vazirani. An introduction to computational learning theory. MIT press, 1994.
