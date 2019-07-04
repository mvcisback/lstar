# L*

[![Build Status](https://travis-ci.com/mvcisback/lstar.svg?branch=master)](https://travis-ci.com/mvcisback/lstar)
[![codecov](https://codecov.io/gh/mvcisback/lstar/branch/master/graph/badge.svg)](https://codecov.io/gh/mvcisback/lstar)
[![PyPI version](https://badge.fury.io/py/lstar.svg)](https://badge.fury.io/py/lstar)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

Implementation of the discriminant tree L* algorithm DFA learning algorithm
provided in [^1].


<!-- markdown-toc start - Don't edit this section. Run M-x markdown-toc-generate-toc again -->
**Table of Contents**

- [L*](#l)
- [Installation](#installation)
- [Usage](#usage)
    - [Membership Queries](#membership-queries)
    - [Equivalence Queries](#equivalence-queries)
    - [All together](#all-together)
- [Learning Moore Machines and DFA-labelers](#learning-moore-machines-and-dfa-labelers)
- [Testing](#testing)
- [TODO](#todo)
- [Footnotes](#footnotes)

<!-- markdown-toc end -->



# Installation

If you just need to use `lstar`, you can just run:

`$ pip install lstar`

For developers, note that this project uses the
[poetry](https://poetry.eustace.io/) python package/dependency
management tool. Please familarize yourself with it and then
run:

`$ poetry install`

# Usage

The main entry point for using this library is the `learn_dfa`
function.

```python
from lstar import learn_dfa
```

This function requires the arguments:
```python
dfa = learn_dfa(
    alphabet= .. ,  #  Alphabet over which the target concept is over.
                    #  Note: Sequence of Hashables.

    membership=..,  #  Function answering whether a given word is in the target
                    #  language.
                    #
                    #  Tuple[Alphabet] -> bool

    find_counter_example=..,  #  Function which takes a hypothesis DFA
                              #  and either returns None or a counter example,
                              #  i.e., an element misclassified by hypothesis
                              #  DFA.
                              #
                              #  DFA -> Union[Tuple[Alphabet], None]

)
```

Below is an example of learning following language over `{0, 1}`:


> The number of 1's in the word is a multiple of 4.


## Membership Queries

We start by defining the membership query function. 

**Note** that this implementation of `lstar` assumes that this
function is either cheap (`O(1)`-ish) to call or is memoized.


```python
from functools import lru_cache

@lru_cache(maxsize=None)  # Memoize member queries 
def is_mult_4(word):
    """Want to learn 4 state counter"""
    return (sum(word) % 4) == 0
```

## Equivalence Queries

Next you need to define a function which given a candidate `DFA`
returns either a counter example that this `DFA` mislabels or `None`.

Note that the `DFA` type used come from the `dfa` package ([link](https://github.com/mvcisback/dfa)).

Below, we simply ask the user to input the counter example as a string.

```python
def ask_human(dfa):
    """User generated counter example.

    An alternative includes sampling or checking against an approximate
    model.
    """
    print(dfa)

    counter_example = input("> Please provide a counter example ").strip()
    counter_example = map(int, counter_example)  #  Language is over {0, 1}.
    counter_example = tuple(counter_example)  # Make counter_example hashable.
    return counter_example if len(counter_example) > 0 else None
```

**Note:** if you are worried that your counter example function may
return an invalid counter_example you can wrap it with the
`validate_ce` decorator.

```python
from lstar import validate_ce

@validate_ce(is_mult_4, retry=True)
def ask_human(dfa):
    ...
```

## All together

```python
dfa = learn_dfa(
    alphabet={0, 1},  #  Possible inputs.
    membership=is_mult_4,  #  Does this sequence belong in the language.
    find_counter_example=ask_human,  #  Use a human for counter examples.
)

assert not dfa.label(())
assert not dfa.label((1,))
assert not dfa.label((1, 1, ))
assert dfa.label((1, 1, 1))
assert dfa.label((1, 1, 0, 1))
```

# Learning Moore Machines and DFA-labelers

By default, `learn_dfa` learns as Deterministic Finite Acceptor;
however, by specifying the `outputs` parameter and adjusting the
`membership` function, one can learn a Deterministic Finite Labeler
(which is isomorphic to a Moore Machine). 

For example, the 4 state counter from before can be modified to output
the current count rather than whether or not the word sums to a
multiple of 4.


```python
def sum_mod_4(state):
    return sum(state) % 4

dfl = learn_dfa(
    alphabet={0, 1},
    membership=sum_mod_4,
    find_counter_example=ask_human,
    outputs={0, 1, 2, 3},
)  # Returns a Deterministic Finite Labeler.

assert dfl.label(()) == 0
assert dfl.label((1,)) == 1
assert dfl.label((1, 1, )) == 2
assert dfl.label((1, 1, 1)) == 3
assert dfl.label((1, 1, 0, 1)) == 3
assert dfl.label((1, 1, 1, 1)) == 0
```

The deterministic labeler can be interpreted as a moore machine by
using the `transduce` method rather than `label`.

```python
assert dfl.transduce(()) == ()
assert dfl.transduce((1,)) == (0,)
assert dfl.transduce((1, 1, )) == (0, 1)
assert dfl.transduce((1, 1, 1)) == (0, 1, 2)
assert dfl.transduce((1, 1, 0, 1)) == (0, 1, 2, 2)
assert dfl.transduce((1, 1, 1, 1, 1)) == (0, 1, 2, 3, 0)
```


# Testing

This project uses pytest. Simply run

`$ poetry pytest`

in the root of the repository.

# TODO

1. [ ] Test counterexample validation decorator.
1. [ ] Add retry old counterexamples decorator.
1. [ ] Default to random sampling counterexample engine


# Footnotes

[^1]: Kearns, Michael J., Umesh Virkumar Vazirani, and Umesh Vazirani. An introduction to computational learning theory. MIT press, 1994.
