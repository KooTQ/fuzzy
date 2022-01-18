"""
Tests for operations on fuzzy membership degree options.

Sanity checks:
  - Any operation must return values within range `[0., 1.]`
  - Any operation take as an argument any value from range
    `[float('-inf'), float('inf')]`
  - Operations can be stacked and combine in any order
  - not t-norm nor s-norm cnot be higher than both of functions
  - not t-norm nor s-norm cannot be lower than both of functions
  - t-norm or s-norm applied on 2 instances of same function `f`
    must result with same results as function `f`

Negation:
  - For any function - double negation must return same
    results as given function

Operators should be tested on:
  - Triangular membership functions
  - Trapezoid membership functions
  - Infinite trapezoid MF
  - combination of any and all of the above
"""
from fuzzy.operators import StrongNegation
from fuzzy.functions import TriangularFunction

import numpy as np

def test_double_strong_negation_on_triangular_membership_functions():
     trial_funct = TriangularFunction(0, 1, 2)
     values = np.linspace(-2, 3, 50)
     degrees_of_memb = np.array([trial_funct(v) for v in values])
     neg_neg_funct = StrongNegation(StrongNegation(trial_funct))
     degrees_of_memb_neg = np.array([neg_neg_funct(v) for v in values])
     assert -1e-5 < np.sum(degrees_of_memb - degrees_of_memb_neg) < 1e-5
