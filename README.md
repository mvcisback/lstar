# L*

[![Build Status](https://travis-ci.com/mvcisback/lstar.svg?branch=master)](https://travis-ci.com/mvcisback/lstar)
[![codecov](https://codecov.io/gh/mvcisback/lstar/branch/master/graph/badge.svg)](https://codecov.io/gh/mvcisback/lstar)
[![PyPI version](https://badge.fury.io/py/lstar.svg)](https://badge.fury.io/py/lstar)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

Implementation of the discriminant tree L* algorithm DFA learning algorithm
provided in [^1].


<!-- markdown-toc start - Don't edit this section. Run M-x markdown-toc-generate-toc again -->
**Table of Contents**

- [Installation](#installation)
- [Usage](#usage)
    - [Label Queries](#label-queries)
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
    inputs= .. ,  #  Inputs over which the target concept is over.
                    #  Note: Sequence of Hashables.

    label=..,  #  Function answering whether a given word is in the target
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


## Label Queries

We start by defining the label query function. 

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

Note that the `DFA` type used comes from the `dfa` package
([link](https://github.com/mvcisback/dfa)).

`lstar` provides two functions to make writing counterexample oracles 
easier.

1. `validate_ce`: Takes a counterexample oracle and retries 
   if returned "counterexample" is not actually a counterexample.
   Useful if using heuristic solver or asking a human.

    ```python
    from lstar import validate_ce

    @validate_ce(is_mult_4, retry=True)
    def ask_human(dfa):
        ...
    ```
2. `iterative_deeping_ce`: This function performs an iterative
   deepening traversal of the candidate dfa and see's if it matches
   the labeler on all tested words.

   ```python
   from lstar import iterative_deeping_ce

   find_ce = iterative_deeping_ce(is_mult_4, depth=10)
   ```


## All together

```python
dfa = learn_dfa(
    inputs={0, 1},  #  Possible inputs.
    label=is_mult_4,  #  Does this sequence belong in the language.
    find_counter_example=iterative_deeping_ce(is_mult_4, depth=10)
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
`label` function, one can learn a Deterministic Finite Labeler
(which is isomorphic to a Moore Machine). 

For example, the 4 state counter from before can be modified to output
the current count rather than whether or not the word sums to a
multiple of 4.


```python
def sum_mod_4(state):
    return sum(state) % 4

dfl = learn_dfa(
    inputs={0, 1},
    label=sum_mod_4,
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

`$ poetry run pytest`

in the root of the repository.

# Similar Libraries
## Python Based
    1. https://github.com/steynvl/inferrer : DFA learning
       library supporting active and passive dfa learning. Active
       learning is based on L* with an observation table. Also
       supports learning NFAs.

   1. https://gitlab.lis-lab.fr/dev/scikit-splearn/ : Library for learning
      weighted automata via the spectral method.

   1. https://pypi.org/project/pylstar/ : Another L* based DFA
      learning library.

## Java Based
   1. https://learnlib.de/ : State of the art automata learning
      toolbox. Supports passive and active learning algorithms for DFAs,
      Mealy Machines, and Visibly Push Down Automata.
   1. https://github.com/lorisdanto/symbolicautomata : Library for
      symbolic automata and symbolic visibly pushdown automata.

# Footnotes

[^1]: Kearns, Michael J., Umesh Virkumar Vazirani, and Umesh Vazirani. An introduction to computational learning theory. MIT press, 1994.
