"""
Tests for operations on fuzzy membership degree options.

Sanity checks:
  - Any operation must return values within range `[0., 1.]`
  - Any operation take as an argument any value from range
    `[float('-inf'), float('inf')]`
  - Operations can be stacked and combine in any order
  - Operations can be stacked many times
  - not t-norm nor s-norm can be higher than both of functions
  - not t-norm nor s-norm can be lower than both of functions
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
import random

import numpy as np

from fuzzy.operators import StrongNegation, TNorm, SNorm
from fuzzy.functions import (
    TriangularFunction, InfiniteTrapezoidFunction
)

from tests.fuzzy.functions.function.test_trapezoid_call import \
    create_random_trapezoid_function, create_random_triangular_function


def test_double_strong_negation_on_triangular_membership_functions() -> None:
    trial_funct = TriangularFunction(0, 1, 2)
    values = np.linspace(-2, 3, 50)
    degrees_of_memb = np.array([trial_funct(v) for v in values])
    neg_neg_funct = StrongNegation(StrongNegation(trial_funct))
    degrees_of_memb_neg = np.array([neg_neg_funct(v) for v in values])
    assert -1e-5 < np.sum(degrees_of_memb - degrees_of_memb_neg) < 1e-5


def test_double_strong_negation_on_triangular_membership_function_n_times(
        n: int = 5
) -> None:
    for _ in range(n):
        trial_funct, left, right = create_random_triangular_function(
            include_positions=True
        )
        values = np.linspace(left - 10, right + 10, 50)
        degrees_of_memb = np.array([trial_funct(v) for v in values])
        neg_neg_funct = StrongNegation(StrongNegation(trial_funct))
        degrees_of_memb_neg = np.array([neg_neg_funct(v) for v in values])
        assert -1e-5 < np.sum(degrees_of_memb - degrees_of_memb_neg) < 1e-5


def test_10_tier_rule_operation_on_infinite_trapezoid_functions() -> None:
    funct1 = InfiniteTrapezoidFunction(0.2, 0.5, 'left')
    funct2 = InfiniteTrapezoidFunction(-0.2, 20, 'left')
    funct3 = InfiniteTrapezoidFunction(20, 20.1, 'right')
    op1 = StrongNegation(funct1)
    op2 = TNorm(op1, funct1)
    op3 = SNorm(op2, funct2)
    op4 = TNorm(funct3, funct1)
    op5 = StrongNegation(op4)
    op6 = TNorm(op4, op5)
    op7 = StrongNegation(funct3)
    op8 = TNorm(op6, op7, funct1)
    op9 = TNorm(op3, funct3)
    op10 = SNorm(op8, op9, op4)
    values = np.linspace(-1, 21, 200)
    for v in values:
        res = op10(v)
        assert 0. <= res <=1


def test_t_norm_not_higher_nor_lower_than_inner_trapezoid_functions() -> None:
    funct1 = create_random_trapezoid_function()
    funct2 = create_random_trapezoid_function()
    funct3 = create_random_trapezoid_function()
    op1 = TNorm(funct1, funct2)
    op2 = TNorm(funct1, funct2, funct3)
    values1 = np.linspace(funct1.lower_boundary - 1,
                          funct1.upper_boundary, 50)
    values2 = np.linspace(funct2.lower_boundary - 1,
                          funct2.upper_boundary, 50)
    values3 = np.linspace(funct3.lower_boundary - 1,
                          funct3.upper_boundary, 50)
    _assert_higher_lower(values1, funct1, funct2, funct3, op1, op2)
    _assert_higher_lower(values2, funct1, funct2, funct3, op1, op2)
    _assert_higher_lower(values3, funct1, funct2, funct3, op1, op2)


def test_s_norm_not_higher_nor_lower_than_inner_trapezoid_functions() -> None:
    funct1 = create_random_trapezoid_function()
    funct2 = create_random_trapezoid_function()
    funct3 = create_random_trapezoid_function()
    op1 = SNorm(funct1, funct2)
    op2 = SNorm(funct1, funct2, funct3)
    values1 = np.linspace(funct1.lower_boundary - 1,
                          funct1.upper_boundary, 50)
    values2 = np.linspace(funct2.lower_boundary - 1,
                          funct2.upper_boundary, 50)
    values3 = np.linspace(funct3.lower_boundary - 1,
                          funct3.upper_boundary, 50)
    _assert_higher_lower(values1, funct1, funct2, funct3, op1, op2)
    _assert_higher_lower(values2, funct1, funct2, funct3, op1, op2)
    _assert_higher_lower(values3, funct1, funct2, funct3, op1, op2)


def _assert_higher_lower(values, f1, f2, f3, op1, op2) -> None:
    for v in values:
        res1 = f1(v)
        res2 = f2(v)
        res3 = f3(v)
        op1_res = op1(v)
        op2_res = op2(v)
        assert op1_res <= max([res1, res2, res3])
        assert op2_res <= max([res1, res2, res3])
        assert op1_res >= min([res1, res2, res3])
        assert op2_res >= min([res1, res2, res3])




def test_t_norm_in_range_0_to_1() -> None:
    funct1 = create_random_trapezoid_function()
    funct2 = create_random_trapezoid_function()
    funct3 = create_random_trapezoid_function()
    op1 = TNorm(funct1, funct2)
    op2 = TNorm(funct1, funct2, funct3)
    values1 = np.linspace(funct1.lower_boundary - 1,
                          funct1.upper_boundary, 50)
    values2 = np.linspace(funct2.lower_boundary - 1,
                          funct2.upper_boundary, 50)
    values3 = np.linspace(funct3.lower_boundary - 1,
                          funct3.upper_boundary, 50)
    _assert_higher_lower(values1, funct1, funct2, funct3, op1, op2)
    _assert_higher_lower(values2, funct1, funct2, funct3, op1, op2)
    _assert_higher_lower(values3, funct1, funct2, funct3, op1, op2)


def test_s_norm_in_range_0_to_1() -> None:
    funct1 = create_random_trapezoid_function()
    funct2 = create_random_trapezoid_function()
    funct3 = create_random_trapezoid_function()
    op1 = SNorm(funct1, funct2)
    op2 = SNorm(funct1, funct2, funct3)
    values1 = np.linspace(funct1.lower_boundary - 1,
                          funct1.upper_boundary, 50)
    values2 = np.linspace(funct2.lower_boundary - 1,
                          funct2.upper_boundary, 50)
    values3 = np.linspace(funct3.lower_boundary - 1,
                          funct3.upper_boundary, 50)
    _assert_0_to_1(values1, op1, op2)
    _assert_0_to_1(values2, op1, op2)
    _assert_0_to_1(values3, op1, op2)


def _assert_0_to_1(values, op1, op2) -> None:
    for v in values:
        op1_res = op1(v)
        op2_res = op2(v)
        assert op1_res <= 1.0
        assert op2_res <= 1.0
        assert op1_res >= 0.0
        assert op2_res >= 0.0


def test_infinite_inputs_triangular_function() -> None:
    triangular_funct = create_random_triangular_function()
    out_low_inf = triangular_funct(float('-inf'))
    assert 0. <= out_low_inf <= 1.
    out_high_inf = triangular_funct(float('inf'))
    assert 0. <= out_high_inf <= 1.


def test_infinite_inputs_trapezoid_function() -> None:
    triangular_funct = create_random_trapezoid_function()
    out_low_inf = triangular_funct(float('-inf'))
    assert 0. <= out_low_inf <= 1.
    out_high_inf = triangular_funct(float('inf'))
    assert 0. <= out_high_inf <= 1.


def test_infinite_inputs_infinite_trapezoid_function() -> None:
    left = random.randint(-100, 100) * (random.random() ** 2)
    right = left + random.randint(1, 10) * (random.random() ** 2)
    neg_left_inf_funct = StrongNegation(InfiniteTrapezoidFunction(
        left, right, 'left'
    ))
    out_low_inf = neg_left_inf_funct(float('-inf'))
    assert 0. <= out_low_inf <= 1.
    out_high_inf = neg_left_inf_funct(float('inf'))
    assert 0. <= out_high_inf <= 1.

    s_normed_right_inf_funct = SNorm(
        InfiniteTrapezoidFunction(left, right, 'right'),
        neg_left_inf_funct
    )
    out_low_inf = s_normed_right_inf_funct(float('-inf'))
    assert 0. == out_low_inf
    out_high_inf = s_normed_right_inf_funct(float('inf'))
    assert 1. == out_high_inf

    t_normed = TNorm(s_normed_right_inf_funct, neg_left_inf_funct)
    out_low_inf = t_normed(float('-inf'))
    assert 0. == out_low_inf
    out_high_inf = t_normed(float('inf'))
    assert 1. == out_high_inf
